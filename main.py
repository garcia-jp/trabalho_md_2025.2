from src.algoritmos import *

def algoritmo_exe(qual, graph):
    if qual == "kruskal":
        # teste kruskal
        result = kruskal(graph)
    elif qual == "boruvka":
        # teste Boruvka
        result = boruvka(graph)
    elif qual == "chu_liu":
        # teste chu-liu/edmonds
        result = chu_liu(graph)
    else:
        raise ValueError("Passe um argumento valido: \"kruskal\", \"buruvka\" ou \"chu_liu\"")
    
    # Saída
    result.gerar_imagem(f"resultado_{qual}")
    graph.gerar_imagem_original(result, f"misto_{qual}")
    graph.gerar_imagem(f"original_{qual}")
    
    return result

if __name__ == '__main__': 
    # Entrada
    caminho = "/home/garcia/Documentos/repo/md_repo/data/grafoT1.json"
    indice = 10

    graph = grafo.Grafo(direcionado=True)
    graph.set_grafo(caminho, indice)
    
    graph.set_root("V2")
    # Passe como primeiro argumento "kruskal", "buruvka" ou "chu_liu"
    result = algoritmo_exe("chu_liu", graph)
