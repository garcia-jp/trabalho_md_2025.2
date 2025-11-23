# Algoritmos de Otimização em Grafos (Matemática Discreta)

Este projeto foi desenvolvido como parte da disciplina de Matemática Discreta. Ele implementa algoritmos fundamentais para encontrar Árvores Geradoras Mínimas (MST) e Arborescências de Custo Mínimo em grafos ponderados.

O sistema utiliza a biblioteca **NetworkX** para manipulação das estruturas de dados e **Matplotlib** para a geração visual dos resultados.

## Algoritmos Implementados

O projeto conta com três algoritmos principais:

1.  **Kruskal**: Para encontrar a MST em grafos **não direcionados**.
2.  **Borůvka**: Para encontrar a MST em grafos **não direcionados**.
3.  **Chu-Liu / Edmonds**: Para encontrar a Arborescência de Custo Mínimo (MST direcionada) em grafos **direcionados**.

## 1. Pré-requisitos

Para executar o projeto, você precisa ter o **Python 3** instalado. Além disso, é necessário instalar as dependências listadas abaixo:

```bash
pip install networkx matplotlib
```

## 2. Configurando o Teste (main.py)

Todo o controle do programa é feito editando o arquivo main.py.

# A. Escolher o Grafo

Os grafos estão no arquivo data/grafoT1.json. Para selecionar um grafo:

    Abra o arquivo data/grafoT1.json e veja a posição do grafo que deseja (a contagem começa em 0).

    No main.py, altere a variável indice:

```Python
# Exemplo: Selecionando o 11º grafo da lista (índice 10)
indice = 10
```
# B. Escolher o Algoritmo

No final do arquivo main.py, localize a chamada da função algoritmo_exe. Você pode passar uma das três opções (string):

    "kruskal"

    "boruvka"

    "chu_liu"

```Python
# Exemplo para rodar o algoritmo de Chu-Liu
result = algoritmo_exe("chu_liu", graph)
```
**Nota Importante:** Se for usar Chu-Liu, o grafo selecionado no JSON deve ter "direcionado": "True" e você deve definir uma raiz válida usando graph.set_root("NomeDoNo").

## 3. Executando o Código

Com o terminal aberto na pasta raiz do projeto, execute:
```Bash
python main.py
```

## 4. Analisando os Resultados

O programa não abre janelas. Ele gera 3 imagens PNG na pasta do projeto para você analisar:

    original_[algoritmo].png:

        Mostra o grafo completo como ele é na entrada.

    resultado_[algoritmo].png:

        Mostra apenas a Árvore/Arborescência resultante (sem as arestas descartadas).

    misto_[algoritmo].png:

        A visualização mais útil. Mostra o grafo original em preto e destaca em azul as arestas que o algoritmo escolheu.

## 5. Adicionando Novos Grafos

Para testar seus próprios casos, edite o arquivo data/grafoT1.json e adicione um novo objeto à lista:

```JSON
{
  "nome": "Meu Grafo de Teste",
  "direcionado": "True",
  "nodes": ["A", "B", "C"],
  "edges": [
    ["A", "B", 10],
    ["B", "C", 5],
    ["A", "C", 20]
  ]
}
```
