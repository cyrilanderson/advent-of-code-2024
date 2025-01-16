import sys
import time
#import re
# import itertools
# import collections

# Relevant powers of two
# 32 = 2**5
# 64 = 2**6
# 2048 = 2**11
# 16777216 = 2**24

funcs = {
    'AND': lambda x, y: x & y,
    'OR': lambda x, y: x | y,
    'XOR': lambda x, y: x ^ y,
}

def read_inputs(file_path):
    with open(file_path, 'r') as file:
        lines = file.read()
    inits, gates = lines.split('\n\n')
    inits = inits.split('\n')
    inits = [line.split(': ') for line in inits]
    inits = {line[0]: line[1] for line in inits}
    #print(inits)
    gates = gates.strip().split('\n')
    gates = [gate.split(' ') for gate in gates]
    # (in1, gate_type, in2, out)
    # E.g. ('svb', 'XOR', 'fsw', 'nwq')
    # gate_type can be 'AND', 'OR', or 'XOR'
    gates = [(gate[0], gate[1], gate[2], gate[4]) for gate in gates]
    # for gate in gates:
    #     print(gate)
    return inits, gates
    
# Takes in dict of initial line names and values, as well as a list of gate tuples
# Returns a dict representing the computational graph
def create_computational_graph(initials, gates):
    comp_graph = {}
    comp_graph['START'] = {
        'type': 'START',
        'send0': set(),
        'send1': set(),
    }

    for key, val in initials.items():
        if val == '1':
            comp_graph['START']['send1'].add(key)
        else:
            comp_graph['START']['send0'].add(key)
        comp_graph[key] = {
            'val': None,
            'type': 'line',
            'outs': set(),
        }
    
    for gate in gates:
        in1 = gate[0]
        gate_type = gate[1]
        in2 = gate[2]
        out = gate[3]
    
        new_gate = {
            'in1': None,
            'in2': None,
            'out': out,
            'type': 'gate',
            'gate_type': gate_type,
        }
        new_gate_name = f"{in1}_{gate_type}_{in2}_{out}"
        comp_graph[new_gate_name] = new_gate
        if in1 not in comp_graph:
            comp_graph[in1] = {
                'val': None,
                'type': 'line',
                'outs': {new_gate_name}
            }
        else:
            comp_graph[in1]['outs'].add(new_gate_name)
        
        if in2 not in comp_graph:
            comp_graph[in2] = {
                'val': None,
                'type': 'line',
                'outs': {new_gate_name}
            }
        else:
            comp_graph[in2]['outs'].add(new_gate_name)
        
        if out not in comp_graph:
            comp_graph[out] = {
                'val': None,
                'type': 'line',
                'outs': set()
            }

    # for key in comp_graph:
    #     print(key, comp_graph[key])
    return comp_graph

# Takes in a dict representing the computational graph
# Starting from 'START' node, runs the graph
# Returns a dict of line names and values
def run_computational_graph(graph):
    start = graph['START']
    queue = []
    for node in start['send1']:
        graph[node]['val'] = 1
        queue.append(node)
    for node in start['send0']:
        graph[node]['val'] = 0
        queue.append(node)
    while queue:
        node = queue.pop(0)
        if graph[node]['type'] == 'line':
            # If node is a line type, next is a gate type 
            # or empty set if an end node
            val = graph[node]['val']
            if graph[node]['outs'] == set():
                continue
            for out in graph[node]['outs']:
                if graph[out]['in1'] == None:
                    graph[out]['in1'] = val
                else:
                    graph[out]['in2'] = val
                queue.append(out)
        if graph[node]['type'] == 'gate':
            # if node is a gate, next is a line
            in1 = graph[node]['in1']
            in2 = graph[node]['in2']
            if in1 != None and in2 != None:
                gate_type = graph[node]['gate_type']
                func = funcs[gate_type]
                val = func(in1, in2)
                out = graph[node]['out']
                graph[out]['val'] = val
            queue.append(out)
    return graph

# Takes in a dict of line names and values
# Using the names starting with 'z' builds up a final binary number
# z00 is least significant bit, z01 is next least significant bit, etc.
# Output result as decimal
def final_result(completed_graph):
    z_nodes = [(node, completed_graph[node]['val']) for node in completed_graph if node[0] == 'z']
    z_nodes = sorted(z_nodes, reverse = True)
    num = ''
    for node in z_nodes:
        num += str(node[1])
    print(num, len(num))
    # print(2**45)
    num = int(num, 2)
    return num



def main():
    start_time = time.time()
    file_path = sys.argv[1]
    initial_values, gates = read_inputs(file_path)
    computational_graph = create_computational_graph(initial_values, gates)
    completed_graph = run_computational_graph(computational_graph)
    # for node in completed_graph:
    #     print(node, completed_graph[node])
    num = final_result(completed_graph)
    print(f"Final result: {num}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_24_problem_1.py <file_path>")
    else:
        main()