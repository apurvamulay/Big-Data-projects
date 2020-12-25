import networkx as nx
import numpy as np

# Create directed graph from edge_list
G = nx.read_edgelist("amazon0302.txt", create_using=nx.DiGraph)


# Get neighbors of activated nodes
def get_neighbors_of_active_nodes(g, new_active):
    neighbors_active_node = []
    for node in new_active:
        neighbors_active_node += g.neighbors(node)

    return neighbors_active_node

# create a dictionary of node to 1/out_degree
def create_node_to_degree_dict(G):
    node_to_degree = dict(G.out_degree)
    for key, val in node_to_degree.items():
        if val != 0:
            node_to_degree[key] = 1 / val

    return node_to_degree


node_to_inverse_degree = create_node_to_degree_dict(G)


# Independent cascade function
def IC(graph_object, S, p, mc):
    # Loop over the Monte-Carlo Simulations
    spread = []
    for i in range(mc):
        print("IC:", i)
        # Simulate propagation process
        new_active, A = S[:], S[:]

        while new_active:
            # 1. Find out-neighbors for each newly active node
            if isinstance(graph_object, nx.DiGraph):
                targets = get_neighbors_of_active_nodes(graph_object, new_active)

            # 2. Determine newly activated neighbors (set seed and sort for consistency)
            success = [True if node_to_inverse_degree[t] < p else False for t in targets]
            new_ones = list(np.extract(success, sorted(targets)))

            # 3. Find newly activated nodes and add to the set of activated nodes
            new_active = list(set(new_ones) - set(A))
            A += new_active

        spread.append(len(A))

    return (np.mean(spread), A)

# Greedy method for cascade maximization
def greedy(g, k, p, mc):
    S, spread = [], []

    # Find k nodes with largest marginal gain
    for _ in range(k):

        best_spread = 0
        nodes_not_in_seed_set = list(set(list(G.nodes)) - set(S))
        for j in nodes_not_in_seed_set:
            node = '' + j
            # Get the spread
            s, temp = IC(g, S + [node], p, mc)

            # Update the winning node and spread so far
            if s > best_spread:
                best_spread, node = s, j

        # Add the selected node to the seed set
        S.append(node)

        # Add estimated spread
        spread.append(best_spread)

    return S, spread


# Parameters for greedy method:
# G = Directed Graph networkx
# k = Budget or initial k node sets to activate = 10
# p = Random probablity of coin flips = 0.5
# mc = Monte-Carlo simulations

seed_set, spread = greedy(G, k=10, p=0.5, mc=10)

print("Greedy Approach")
print(seed_set)
