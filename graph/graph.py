import pandas as pd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import community

# ラッパーのデータをデータフレーム化
df_name = pd.read_csv("directors.csv", header=None)
df_ft = pd.read_csv("combinations.csv", header=None)

graph = nx.Graph()
graph.add_nodes_from(list(df_name[0]))
graph.add_weighted_edges_from(df_ft.values.tolist())
edges = graph.edges(data=True)
for (u, v, d) in list(edges):
    if d["weight"] <= 2:
        graph.remove_edge(u, v)
eigen_cent = nx.pagerank(graph)
print(eigen_cent)

pos = nx.spring_layout(graph, k=1.8)
#pos = nx.circular_layout(graph)
nx.draw_networkx_labels(graph, pos, font_family="TakaoPGothic", font_size=13)
edge_width = [ d["weight"]*0.3 for (u,v,d) in graph.edges(data=True)]
nx.draw_networkx_edges(graph, pos, alpha=1, edge_color="#2eccfa", width=edge_width)
node_size = [10000 * size for size in list(eigen_cent.values())]
nx.draw_networkx_nodes(graph, pos, alpha=0.6, node_color="#f7819f", node_size=node_size)

plt.axis("off")
plt.show()