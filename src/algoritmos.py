import networkx as nx
import src.grafo as grafo

def kruskal(graph):
    # graph = grafo.Grafo()
    # graph.grafo = nx.Graph()
    resultado = grafo.Grafo()

    nodes = graph.grafo.nodes()
    resultado.add_nodes(nodes)

    # Extrair edges com os seus pesos
    edges = []
    for u, v, data in graph.grafo.edges(data=True):
        w = data.get('weight', 0)
        edges.append((u, v, w))
    
    edges = sorted(edges, key=lambda item: item[2])

    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}

    for u, v, weight in edges:
        x = graph.encontrar(parent, u)
        y = graph.encontrar(parent, v)
        if x != y:
            resultado.add_edge(u, v, weight)
            graph.uniao(parent, rank, x, y)
    return resultado

def boruvka(graph):
    # Apagar
    # graph = grafo.Grafo()
    # graph.grafo = nx.Graph()
    
    # Inicialização
    resultado = grafo.Grafo()
    nodes = graph.grafo.nodes()
    resultado.add_nodes(nodes)

    numTrees = len(nodes)
    MSTweight = 0

    nodes = graph.grafo.nodes()
    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}

    while numTrees > 1:
        cheapest = {}

        # Encontrar a aresta mais barata em cada componente
        for u, v, data in graph.grafo.edges(data=True):
            w = data.get('weight', 0)

            # Encontrar raiz da componente de cada um dos vértices
            raiz_u = graph.encontrar(parent, u)
            raiz_v = graph.encontrar(parent ,v)

            if raiz_u != raiz_v:     
                if raiz_u not in cheapest or cheapest[raiz_u][2] > w:
                    cheapest[raiz_u] = [u,v,w] 

                if raiz_v not in cheapest or cheapest[raiz_v][2] > w:
                    cheapest[raiz_v] = [u,v,w]

        num_unioes_nesta_fase = 0
        
        # Itera sobre as arestas selecionadas (values do dicionário)
        for u, v, w in cheapest.values():
            raiz_u = graph.encontrar(parent, u)
            raiz_v = graph.encontrar(parent, v)

            if raiz_u != raiz_v:
                # Realiza a união
                graph.uniao(parent, rank, raiz_u, raiz_v)
                
                # Adiciona ao resultado
                resultado.add_edge(u, v, w)
                MSTweight += w

                numTrees -= 1
                num_unioes_nesta_fase += 1
                # print(f"Aresta adicionada: {u} -- {v} (Peso: {w})")
        
        # Segurança: Se rodou uma fase inteira e não uniu nada, termina (evita loop infinito em desconexos)
        if num_unioes_nesta_fase == 0:
            break

    # print ("Weight of MST is %d" % MSTweight)
    return resultado

def chu_liu_objetivo(graph):
    # Apagar
    # graph = grafo.Grafo(direcionado=True)
    # graph.grafo = nx.DiGraph()
    
    resultado = grafo.Grafo(direcionado=True)
    mst_nx = nx.minimum_spanning_arborescence(graph.grafo, attr='weight', default=graph.root)

    resultado.set_nx(mst_nx)

    return resultado

def chu_liu(graph):
    if not graph.direcionado:
        raise ValueError("Chu-Liu requer grafo DIRECIONADO.")
        
    mst_nx = _cle_recursivo(graph.grafo, graph.root)
    
    resultado = grafo.Grafo(direcionado=True)
    
    resultado.set_nx(mst_nx)
    resultado.nome = "Resultado Chu-Liu"
    return resultado

def _cle_recursivo(G, raiz):
    # --- PASSO 1: OLHAR GULOSO (O que o olho escolhe primeiro?) ---
    # Seleciona a aresta de menor peso entrando em cada nó
    selecionadas = []
    for v in G.nodes():
        if v != raiz:
            # Pega todas as arestas (u->v) e escolhe a mais barata
            entradas = G.in_edges(v, data='weight')
            if entradas:
                selecionadas.append(min(entradas, key=lambda x: x[2]))

    # Cria um grafo temporário só com essas arestas para ver se tem ciclo
    R = nx.DiGraph()
    R.add_nodes_from(G.nodes())
    R.add_edges_from([(u, v, {'weight': w}) for u, v, w in selecionadas])

    # --- PASSO 2: TEM CICLO? (A verificação visual) ---
    try:
        # O networkx faz o trabalho sujo de achar o ciclo pra gente
        ciclo = list(nx.find_cycle(R))
        nos_do_ciclo = set(u for u, v in ciclo)
        super_no = f"super_{next(iter(nos_do_ciclo))}" # Nome do 'nó fundido'
    except nx.NetworkXNoCycle:
        return R # Se não tem ciclo, acabou! É a resposta.

    # --- PASSO 3: CONTRAÇÃO (A matemática do "desconto") ---
    # G' é o grafo novo com o ciclo virando um pontinho
    G_prime = nx.DiGraph()
    
    # Descobre quanto custa a aresta interna do ciclo para cada nó (para dar o desconto)
    # Ex: se A->B custa 5 dentro do ciclo, entrar em B por fora ganha desconto de 5
    peso_interno = {v: w for u, v, w in selecionadas if v in nos_do_ciclo}
    
    # Guarda qual aresta original corresponde à nova (para desfazer depois)
    # Chave: (u_novo, v_novo) -> Valor: (u_orig, v_orig, w_orig)
    mapa = {}

    for u, v, data in G.edges(data=True):
        w = data['weight']
        
        # Aresta entra no ciclo? (Vem de fora -> Ciclo)
        if u not in nos_do_ciclo and v in nos_do_ciclo:
            novo_w = w - peso_interno[v] # AQUI ESTÁ A MÁGICA
            # Adiciona se for melhor que a que já temos
            if novo_w < G_prime.get_edge_data(u, super_no, default={'weight': float('inf')})['weight']:
                G_prime.add_edge(u, super_no, weight=novo_w)
                mapa[(u, super_no)] = (u, v, w)
        
        # Aresta sai do ciclo? (Ciclo -> Vai pra fora)
        elif u in nos_do_ciclo and v not in nos_do_ciclo:
            if w < G_prime.get_edge_data(super_no, v, default={'weight': float('inf')})['weight']:
                G_prime.add_edge(super_no, v, weight=w)
                mapa[(super_no, v)] = (u, v, w)
        
        # Aresta não tem nada a ver com o ciclo?
        elif u not in nos_do_ciclo and v not in nos_do_ciclo:
            G_prime.add_edge(u, v, weight=w)

    # --- PASSO 4: RESOLVE O PROBLEMA MENOR (Recursão) ---
    arvore_contraida = _cle_recursivo(G_prime, raiz)

    # --- PASSO 5: EXPANSÃO (Abre o super nó) ---
    resultado = nx.DiGraph()
    no_quebrado = None

    for u, v, data in arvore_contraida.edges(data=True):
        # Se a aresta conecta ao super_no, recuperamos a original
        if u == super_no or v == super_no:
            orig_u, orig_v, orig_w = mapa[(u, v)]
            resultado.add_edge(orig_u, orig_v, weight=orig_w)
            
            # Se essa aresta ENTRA no ciclo, anotamos quem ela atingiu
            if v == super_no:
                no_quebrado = orig_v 
        else:
            resultado.add_edge(u, v, weight=data['weight'])

    # Adiciona o ciclo de volta, MENOS a aresta que apontava para onde entramos
    for u, v, w in selecionadas:
        if v in nos_do_ciclo and v != no_quebrado:
            resultado.add_edge(u, v, weight=w)

    return resultado

if __name__ == "__main__":
    # Entrada
    caminho = "/home/garcia/Documentos/repo/md_repo/data/grafoT1.json"
    graph = grafo.Grafo()
    graph.set_grafo(caminho, 2)

    # teste chu-liu/edmonds
    result = chu_liu(graph, 1)

    # Saída
    result.gerar_imagem("resultado")
    graph.gerar_imagem_original(result, "misto")
    graph.gerar_imagem("original")