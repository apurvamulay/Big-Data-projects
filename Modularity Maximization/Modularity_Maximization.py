# Q 3c. Find 3 communities in Graph 6.8 in the Textbook by performing modularity maximization.
# You can use the code you use for Problem 4 to perform this faster.

import community
import networkx as nx

G = nx.Graph(directed=False)
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])

G.add_edges_from([(1, 2),(1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7),
                  (5, 6),(5, 7),(6, 7),(6, 8),(7, 8),(8, 9)])

fp = open("output-Q3.txt", "w")

adj_mat = nx.to_numpy_matrix(G)
fp.write("\n Adjacency Matrix:" + str(adj_mat))

def modularity_maximization(G):
    return community.community_louvain.best_partition(G, randomize=False )


mod_predictions = modularity_maximization(G)
fp.write("\n 3 communities are: {0, 1, 2}:" + "\n")
fp.write(str(mod_predictions))


modularity = community.modularity(mod_predictions, G)
fp.write("\n Modularity (Q) = " + str(modularity))