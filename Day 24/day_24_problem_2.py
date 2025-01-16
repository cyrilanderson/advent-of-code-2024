import sys
import time
#import re
# import itertools
# import collections


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
def get_z_result(completed_graph):
    z_nodes = [(node, completed_graph[node]['val']) for node in completed_graph if node[0] == 'z']
    z_nodes = sorted(z_nodes, reverse = True)
    num_str = ''
    for node in z_nodes:
        num_str += str(node[1])
    # print(2**45)
    num = int(num_str, 2)
    #print(num_str, len(num_str))
    return num_str, num

# This verifies that two nodes share a gate of a certain type. If so, returns True and the gate name
def share_gate(comp_graph, in1, in2, gate_type):
    in1_gates = comp_graph[in1]['outs']
    in2_gates = comp_graph[in2]['outs']
    shared_gates = in1_gates.intersection(in2_gates)
    for gate in shared_gates:
        if comp_graph[gate]['gate_type'] == gate_type:
            return True, gate
    return False, None

def find_gate_partner(comp_graph, gate_type, in1):
    in1_gates = comp_graph[in1]['outs']
    for gate in in1_gates:
        if comp_graph[gate]['gate_type'] == gate_type:
            gate_in1, gate_in2 = comp_graph[gate]['in1'], comp_graph[gate]['in2']
            if gate_in1 == in1:
                return gate_in2
            else:
                return gate_in1
    return None

def check_gates(comp_graph, x_init_labels, y_init_labels, z_labels):
    swap_set = set()

    # verify the 0th bit
    in1 = x_init_labels[0]
    in2 = y_init_labels[0]
    out = z_labels[0]
    check_xor, gate1 = share_gate(comp_graph, in1, in2, 'XOR')
    check_and, gate2 = share_gate(comp_graph, in1, in2, 'AND')
    if check_xor:
        output = comp_graph[gate1]['out']
        if output != out:
            swap_set.add(output)
            swap_set.add(out)
    
    # The result of the and gate is the carry bit and becomes the prev for the next step
    if check_and:
        prev = comp_graph[gate2]['out']

    # We looked at the 0th bit, let's look at the rest
    x_init_labels = x_init_labels[1:]
    y_init_labels = y_init_labels[1:]
    z_labels = z_labels[1:]

    # Verify the nth bit where n >= 1
    for in_out_triplet in zip(x_init_labels, y_init_labels, z_labels):
        in1 = in_out_triplet[0]
        in2 = in_out_triplet[1]
        out = in_out_triplet[2]
        check_xor1, gate_xor1 = share_gate(comp_graph, in1, in2, 'XOR')
        check_and1, gate_and1 = share_gate(comp_graph, in1, in2, 'AND')
        if check_xor1:
            out_xor1 = comp_graph[gate_xor1]['out']
            # See if the ouput of the previous XOR gate and the prev carry bit share an XOR gate as expected 
            check_xor2, gate_xor2 = share_gate(comp_graph, out_xor1, prev, 'XOR')
            if check_xor2:
                out_xor2 = comp_graph[gate_xor2]['out']
                if out_xor2 != out:
                    swap_set.add(out_xor2)
                    swap_set.add(out)
            else:
                partner = find_gate_partner(comp_graph, 'XOR', out_xor1)
                if partner:
                    swap_set.add(partner)
                    swap_set.add(prev)
                else:
                    pass


        if check_and1:
            pass 
    



    return swap_set


def get_z_nodes(comp_graph):
    return sorted([node for node in comp_graph if node[0] == 'z'])

# gates is a list of 4-tuples
# swap is a 2-tuple
def perform_swap(gates, swap):
    out1 = swap[0]
    out2 = swap[1]
    gate1 = [gate for gate in gates if gate[3] == out1][0]
    gate2 = [gate for gate in gates if gate[3] == out2][0]
    gate1_new = (gate1[0], gate1[1], gate1[2], out2)
    gate2_new = (gate2[0], gate2[1], gate2[2], out1)
    gates.remove(gate1)
    gates.remove(gate2)
    gates.append(gate1_new)
    gates.append(gate2_new)
    return gates

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    inits, gates = read_inputs(file_path)


    swaps = [('nwq', 'z36'), ('mdb', 'z22'), ('z18', 'fvw'), ('grf', 'wpq')]
    for swap in swaps:
        gates = perform_swap(gates, swap)
    # print("Gates:")
    # for gate in gates:
    #     print(gate)

    #print(f"Initial values: {inits}")
    print(f"Number of initial values: {len(inits)}")
    x = [(k, inits[k]) for k in inits if k[0] == 'x']
    y = [(k, inits[k]) for k in inits if k[0] == 'y']
    # print(f"First number: {x}")
    # print(f"Second number: {y}")
    x_init_vals = [inits[k] for k in inits if k[0] == 'x']
    x_init_labels = [k for k in inits if k[0] == 'x']
    x_inits_string = "".join(x_init_vals)[::-1]
    y_init_vals = [inits[k] for k in inits if k[0] == 'y']
    y_init_labels = [k for k in inits if k[0] == 'y']
    y_inits_string = "".join(y_init_vals)[::-1]
    print(f"x input as binary: {x_inits_string}, length: {len(x_inits_string)}")
    print(f"x input as decimal: {int(x_inits_string, 2)}")
    print(f"y input as binary: {y_inits_string}, length: {len(y_inits_string)}")
    print(f"y input as decimal: {int(y_inits_string, 2)}")
    target_output = int(x_inits_string, 2) + int(y_inits_string, 2)
    
    ors = [gate for gate in gates if gate[1] == 'OR']
    ands = [gate for gate in gates if gate[1] == 'AND']
    xors = [gate for gate in gates if gate[1] == 'XOR']
    # print(f"ANDs: {len(ands)}")
    # print(f"XORs: {len(xors)}")
    # print(f"ORs: {len(ors)}")

    computational_graph = create_computational_graph(inits, gates)
    # for node in computational_graph:
    #     print(node, computational_graph[node])
    # z_nodes = get_z_nodes(computational_graph)
    # print(f"z nodes: {z_nodes}")

    # anomalous_z_output_gates = [gate for gate in gates if gate[3][0] == 'z' and gate[3] != 'z45' and gate[1] != 'XOR']
    # print("Gates outputting a z that are not XOR gates and not last OR gate:")
    # for gate in anomalous_z_output_gates:
    #     print(gate)
    
    # anomalous_xor_gates = [gate for gate in gates if gate[0][0] not in ['x', 'y'] and  gate[1] == 'XOR' and gate[2][0] not in ['x', 'y'] and gate[3][0] != 'z']
    # print("XOR gates with non-x/y inputs and non-z outputs:")
    # for gate in anomalous_xor_gates:
    #     print(gate)

    # nwg_gates = [gate for gate in gates if gate[0] == 'nwg' or gate[2] == 'nwg' or gate[3] == 'nwg']
    # print("Gates with nwg as input or output:")
    # for nwg_gate in nwg_gates:
    #     print(nwg_gate)
    
    # cjb_gates = [gate for gate in gates if gate[0] == 'cjb' or gate[2] == 'cjb' or gate[3] == 'cjb']
    # print("Gates with cjb as input or output:")
    # for cjb_gate in cjb_gates:
    #     print(cjb_gate)

    # kqr_gates = [gate for gate in gates if gate[0] == 'kqr' or gate[2] == 'kqr' or gate[3] == 'kqr']
    # print("Gates with kqr as input or output:")
    # for kqr_gate in kqr_gates:
    #     print(kqr_gate)

    # x18_gates = [gate for gate in gates if gate[0] == 'x18' or gate[2] == 'x18']
    # print("Gates with x18 as input:")
    # for x18_gate in x18_gates:
    #     print(x18_gate)     

    # gdw_gates = [gate for gate in gates if gate[0] == 'gdw' or gate[2] == 'gdw']
    # print("Gates with gdw as input:")
    # for gdw_gate in gdw_gates:
    #     print(gdw_gate)

    # fvw_gates = [gate for gate in gates if gate[0] == 'fvw' or gate[2] == 'fvw']
    # print("Gates with fvv as input:")
    # for fvw_gate in fvw_gates:
    #     print(fvw_gate)

    # x00_gates = [gate for gate in gates if gate[0] == 'x00' or gate[2] == 'x00']
    # print("Gates with x00 as input:")
    # for x00_gate in x00_gates:
    #     print(x00_gate)

    # y00_gates = [gate for gate in gates if gate[0] == 'y00' or gate[2] == 'y00']
    # print("Gates with y00 as input:")
    # for y00_gate in y00_gates:
    #     print(y00_gate)

    # x01_gates = [gate for gate in gates if gate[0] == 'x01' or gate[2] == 'x01']
    # print("Gates with x01 as input:")
    # for x01_gate in x01_gates:
    #     print(x01_gate)
    
    # y01_gates = [gate for gate in gates if gate[0] == 'y01' or gate[2] == 'y01']
    # print("Gates with y01 as input:")
    # for y01_gate in y01_gates:
    #     print(y01_gate)

    # ppj_gates = [gate for gate in gates if gate[0] == 'ppj' or gate[2] == 'ppj']
    # print("Gates with ppj as input:")
    # for ppj_gate in ppj_gates:
    #     print(ppj_gate)

    # mtd_gates = [gate for gate in gates if gate[0] == 'mtd' or gate[2] == 'mtd']
    # print("Gates with mtd as input:")
    # for mtd_gate in mtd_gates:
    #     print(mtd_gate)
    
    # dsm_gates = [gate for gate in gates if gate[0] == 'dsm' or gate[2] == 'dsm']
    # print("Gates with dsm as input:")
    # for dsm_gate in dsm_gates:
    #     print(dsm_gate)

    # x05_gates = [gate for gate in gates if gate[0] == 'x05' or gate[2] == 'x05']
    # print("Gates with x05 as input:")
    # for x05_gate in x05_gates:
    #     print(x05_gate)
    
    # y05_gates = [gate for gate in gates if gate[0] == 'y05' or gate[2] == 'y05']
    # print("Gates with y05 as input:")
    # for y05_gate in y05_gates:
    #     print(y05_gate)
    
    # grf_gates = [gate for gate in gates if gate[0] == 'grf' or gate[2] == 'grf']
    # print("Gates with grf as input:")
    # for grf_gate in grf_gates:
    #     print(grf_gate)
    
    # wpq_gates = [gate for gate in gates if gate[0] == 'wpq' or gate[2] == 'wpq']
    # print("Gates with wpq as input:")
    # for wpq_gate in wpq_gates:
    #     print(wpq_gate)


    

    completed_graph = run_computational_graph(computational_graph)
    # for node in completed_graph:
    #     print(node, completed_graph[node])
    num_str, num = get_z_result(completed_graph)
    print(f"Actual output as bin value: {num_str}, length: {len(num_str)}")
    print(f"Target bin sum for x and y: {bin(target_output)[2:]}, length: {len(bin(target_output)[2:])}")
    print(f"Actual binary equals target binary: {num_str == bin(target_output)[2:]}")
    print(f"Final result as decimal: {num}")
    print(f"Expected decimal sum of x and y: {target_output}")
    print(f"Actual decimal equals target: {num == target_output}")   
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_24_problem_1.py <file_path>")
    else:
        main()