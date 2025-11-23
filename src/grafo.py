import matplotlib
matplotlib.use('Agg')
import networkx as nx
import matplotlib.pyplot as plt
import json

class Grafo:
    """Não trata erros contra a propria lógica descrita."""
    def __init__(self, direcionado=False) -> None:
        self.direcionado = direcionado
        if direcionado:
            self.grafo = nx.DiGraph()
            self.root = ""
        else:
            self.grafo = nx.Graph()

        self.nome = "Grafo"

    def add_node(self, v):
        self.grafo.add_node(v)

    def add_nodes(self, v):
        self.grafo.add_nodes_from(v)

    def add_edge(self, a, b, w):
        self.grafo.add_edge(a, b, weight=w)

    def add_edges(self, k):
        # Se k = [[a1, b1, w1], [a2, b2, w2], ...]
        self.grafo.add_weighted_edges_from(k)
    
    def set_root(self, root):
        self.root = root

    def set_grafo(self, caminho, indice=0):

        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = json.load(arquivo)
            
            self.direcionado = isinstance(self.grafo, nx.DiGraph)
            if conteudo[indice]["direcionado"] == "True":
                self.grafo = nx.DiGraph()
                self.root = conteudo[indice]["nodes"][0]
            elif conteudo[indice]["direcionado"] == "False":
                self.grafo = nx.Graph()
            else:
                raise ValueError("Argumento 'direcionado' deve ser \"True\" ou \"False\".")

            self.nome = str(conteudo[indice]["nome"])
            self.add_nodes(conteudo[indice]["nodes"])
            self.add_edges(conteudo[indice]["edges"])

    def set_nx(self, nx_graph):
        self.grafo = nx_graph.copy()
        self.direcionado = isinstance(nx_graph, nx.DiGraph)

    def encontrar(self, parent, i):
        if parent[i] == i:
            return i
        # Recursão com compressão de caminho
        parent[i] = self.encontrar(parent, parent[i])
        return parent[i]

    def uniao(self, parent, rank, x, y):
        raiz_x = self.encontrar(parent, x)
        raiz_y = self.encontrar(parent, y)

        # Se já estão no mesmo conjunto, não faz nada
        if raiz_x == raiz_y:
            return False

        # União por Rank
        if rank[raiz_x] < rank[raiz_y]:
            parent[raiz_x] = raiz_y
        elif rank[raiz_x] > rank[raiz_y]:
            parent[raiz_y] = raiz_x
        else:
            parent[raiz_y] = raiz_x
            rank[raiz_x] += 1
            
        return True

    def __str__(self):
        tipo = "direcionado" if self.direcionado else "não-direcionado"
        return f"Grafo {tipo} | V={self.grafo.number_of_nodes()} E={self.grafo.number_of_edges()}"

    def gerar_imagem(self, title=""):
        """Desenha o grafo usando Matplotlib."""
        title = self.nome if title == "" else title

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.grafo)  # Layout de força elástica
        
        # Desenha nós e arestas
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_weight='bold', arrows=self.direcionado)
        
        # Desenha os pesos das arestas
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)
        
        plt.title(title)
        plt.savefig(title, dpi=300, bbox_inches='tight')

    def gerar_imagem_original(self, result, title=""):
        """
        Gera uma imagem do grafo original (self), destacando em AZUL 
        as arestas que estão presentes no objeto 'result'.
        """
        # Define o título padrão ou o passado
        titulo_final = title if not title == "" else f"{self.nome}_com_destaque"

        plt.figure(figsize=(8, 6))
        
        pos = nx.spring_layout(self.grafo, seed=42) 
        
        edge_colors = []
        widths = []
        
        for u, v in self.grafo.edges():
            if result.grafo.has_edge(u, v):
                edge_colors.append('blue')  # Destaca a aresta da solução
                widths.append(2.5)          # Deixa um pouco mais grossa
            else:
                edge_colors.append('black') # Aresta normal do grafo original
                widths.append(1.0)
        
        # Desenha as cores
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_weight='bold', arrows=self.direcionado,
                edge_color=edge_colors, width=widths)
        
        # Desenha os pesos
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels)
        
        plt.title(titulo_final)
        plt.savefig(titulo_final, dpi=300, bbox_inches='tight')
        
if __name__ == "__main__":
    grafinho = Grafo()
    a = int(input())
    grafinho.set_grafo("/home/garcia/Documentos/repo/md_repo/data/grafoT1.json", a)
        
    grafinho.gerar_imagem("teste")