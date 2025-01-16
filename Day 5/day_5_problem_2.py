import sys
from functools import cmp_to_key

def read_sections(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')
    
    section1 = []
    section2 = []
    section = 1
    
    for line in lines:
        if line.strip() == '':
            section = 2
            continue
        
        if section == 1:
            section1.append(line)
        else:
            section2.append(line)
    
    return section1, section2

# Takes in a section of lines from the input file
# Each line is a comma-separated list of number strings
# Returns a list of lists of number strings
def extract_sequences(section):
    sequences = []
    for line in section:
        sequence = line.split(',')
        sequences.append([num for num in sequence])
    print(len(sequences))
    return sequences

def create_graph(section):
    graph = {}
    for line in section:
        line = line.split('|')
        node = line[0]
        if node in graph:
            graph[node].append(line[1])
        else:
            graph[node] = [line[1]]
            if line[1] not in graph:
                graph[line[1]] = []
    return graph

# def is_topological(graph, node_list):
#     # Step 1: Calculate in-degrees of all nodes
#     in_degree = {node: 0 for node in node_list}
#     for node in node_list:
#         relevant_adjacent = [adj for adj in graph[node] if adj in node_list]
#         for n in relevant_adjacent:
#             in_degree[n] += 1
#     # Step 2: Traverse the node_list and check the in-degrees
#     for node in node_list:
#         if in_degree[node] != 0:
#             return False
#         relevant_adjacent = [adj for adj in graph[node] if adj in node_list]
#         for adjacent in relevant_adjacent:
#             in_degree[adjacent] -= 1
#     return True

def comparator(node_a, node_b):
    if node_b in graph[node_a]:
        return -1
    elif node_a in graph[node_b]:
        return 1
    else:
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        section1, section2 = read_sections(file_path)
        graph = create_graph(section1)
        #print(graph)
        sequences_to_check = extract_sequences(section2)
        #print(sequences_to_check)
        total = 0
        for sequence in sequences_to_check:
           sorted_seq = sorted(sequence, key = cmp_to_key(comparator))
           if sequence != sorted_seq:
           #if not is_topological(graph, sequence):
               #sorted_seq = sorted(sequence, key = cmp_to_key(comparator))
               length = len(sorted_seq)
               middle_index = length // 2
               total += int(sorted_seq[middle_index])
        print(total)
