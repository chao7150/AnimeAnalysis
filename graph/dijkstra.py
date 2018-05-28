import networkx as nx

G = nx.DiGraph()
G.add_path([3, 5, 6, 1, 0, 2, 7, 8, 9, 6])
G.add_path([3, 0, 6, 4, 2, 7, 1, 9, 8, 5])

nx.nx_agraph.view_pygraphviz(G, prog='fdp')
