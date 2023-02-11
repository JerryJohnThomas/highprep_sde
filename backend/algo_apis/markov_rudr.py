from .rudr import *
import community as community_louvain

# Compute Markov Clusters

# Compute Markov Clusters
def louvian_clusters(node_travel_distance, positions, draw=False):
    network = nx.from_numpy_array(np.matrix(node_travel_distance))
    partition = community_louvain.best_partition(network)
    # if draw:

    #     # draw the graph
    #     # color the nodes according to their partition
    #     cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    #     nx.draw_networkx_nodes(node_travel_distance, positions, partition.keys(), node_size=40,
    #                         cmap=cmap, node_color=list(partition.values()))
    #     nx.draw_networkx_edges(node_travel_distance, positions, alpha=0.5)
    #     plt.show()
    clusters_dict = dict()
    for i in partition:
        if partition[i] in clusters_dict.keys():
            clusters_dict[partition[i]] += [i]
        else:
            clusters_dict[partition[i]] = [i]
    clusters = list(clusters_dict.values())
    if draw:
        matrix = nx.to_scipy_sparse_array(network)
        mc.draw_graph(matrix, clusters, pos=positions,
                      node_size=50, with_labels=False, edge_color="grey")
    return clusters


def markov_clusters(node_travel_distance, positions, draw=False):
    network = nx.from_numpy_array(np.matrix(node_travel_distance))
    # print(node_travel_distance)
    # print(network)

    # then get the adjacency matrix (in sparse form)
    matrix = nx.to_scipy_sparse_array(network)
    min_modularity_cluster_set = []
    min_modularity = -1

    # perform clustering using different inflation values from 1.5 and 2.5
    # for each clustering run, calculate the modularity
    for inflation in [i / 10 for i in range(11, 25)]:
        result = mc.run_mcl(matrix, inflation=inflation)
        clusters = mc.get_clusters(result)
        Q = mc.modularity(matrix=result, clusters=clusters)
        if Q > min_modularity:
            min_modularity_cluster_set = clusters
            min_modularity = Q

    # print(min_modularity_cluster_set)
    if draw:
        # print(min_modularity_cluster_set)
        mc.draw_graph(matrix, min_modularity_cluster_set, pos=positions,
                      node_size=50, with_labels=False, edge_color="grey")

    return min_modularity_cluster_set