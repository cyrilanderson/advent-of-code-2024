import sys
import time
import networkx as nx


def read_inputs(file_path):
    pairs = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        line = line.split("-")
        pair = (line[0], line[1])
        pairs.add(pair)
    #print(pairs)
    return pairs
    
# def create_graph(pairs):
#     graph = {}
#     for pair in pairs:
#         if pair[0] not in graph:
#             graph[pair[0]] = set()
#         if pair[1] not in graph:
#             graph[pair[1]] = set()
#         graph[pair[0]].add(pair[1])
#         graph[pair[1]].add(pair[0])
#     return graph

def get_nodes(pairs):
    nodes = set()
    for pair in pairs:
        nodes.add(pair[0])
        nodes.add(pair[1])
    return nodes

# def find_three_cycles(graph):
#     three_cycles = set()
#     for node in graph:
#         for neighbor in graph[node]:
#             for neighbor2 in graph[neighbor]:
#                 if node in graph[neighbor2]:
#                     three_cycles.add(tuple(sorted([node, neighbor, neighbor2])))
#     return three_cycles

# def find_triplets(t_pairs, nodes, pairs):
#     triplets = set()
#     for t_pair in t_pairs:
#         other_nodes = {node for node in nodes if node not in t_pair}
#         for node in other_nodes:
#             if ((t_pair[0], node) in pairs or (node, t_pair[0]) in pairs) and ((t_pair[1], node) in pairs or (node, t_pair[1]) in pairs):
#                 triplet = tuple(sorted([t_pair[0], t_pair[1], node]))
#                 triplets.add(triplet)
#     return triplets

def find_largest_clique(edges, nodes):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    cliques = nx.find_cliques(graph)
    largest_clique = max(cliques, key=len)
    return largest_clique


# def find_t_nodes(graph):
#     t_nodes = {node: graph[node] for node in graph if node.startswith("t")}
#     return t_nodes

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    edges = read_inputs(file_path)
    nodes = get_nodes(edges)
    #print(f"Number of nodes: {len(nodes)}")
    #graph = create_graph(pairs)
    #t_nodes = find_t_nodes(graph)
    largest_clique = find_largest_clique(edges, nodes)
    sorted_clique = sorted(largest_clique)
    clique_str = ",".join(sorted_clique)
    print(f"Largest clique: {clique_str}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_25_problem_1.py <file_path>")
    else:
        main()