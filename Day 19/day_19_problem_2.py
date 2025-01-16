import sys
import time

def read_towels_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')
    
    section1 = ""
    designs = []
    section = 1
    
    for line in lines:
        line = line.strip()
        if line == '':
            section = 2
            continue
        
        if section == 1:
            section1 += ' ' + line
        else:
            designs.append(line)

    towels = section1.strip().split(', ')
    # print(f"Towel types: {towels}")
    towels_trie = {
            'children': {},
            'word_finished': False,
    }
    for towel in towels:
        current_node = towels_trie
        for idx, char in enumerate(towel):
            if char not in current_node['children']:
                new_node = {                        
                    'children': {},
                    'word_finished': False
                }
                current_node['children'][char] = new_node
                current_node = current_node['children'][char]
            else:
                current_node = current_node['children'][char]
            if idx == len(towel) - 1:
                current_node['word_finished'] = True
    return towels, towels_trie, designs

# NOTE. This is working, and efficient as far as iteratively handling, but is too slow to be practical.
# Get through design 1 (no valid arrangements) nearly instantly, design 2 takes a while with ~ 80 million combinations
# There are 400 designs. Need to recognize repeated elements in the computation. Reddit is talking about memoization. 
# Let me think this through more.

# def count_valid_arrangements(trie, design):
#     trie_branch = trie
#     design_segment = design
#     stack = [(trie_branch, design_segment)]
#     valid_designs_implementations = 0
#     while stack:
#         trie_branch, design_segment = stack.pop()
#         if trie_branch['word_finished']:
#             if not design_segment:
#                 valid_designs_implementations += 1
#                 # print(f"Found a valid design implementation: {implementation} for {design}")
#                # print(f"Running designs count: {valid_designs_implementations}")
#             else:
#                 #impl_start_new_word = implementation + ['']
#                 stack.append((trie, design_segment))
#         if design_segment:
#             char = design_segment[0]
#             if char in trie_branch['children']:
#                 #implementation[-1] += char
#                 stack.append((trie_branch['children'][char], design_segment[1:]))

#     return valid_designs_implementations     

# Stores all results of counting valid arangements for a design segment starting at the top of the trie
arrangement_search_cache = {}

# This is the recursive version of the above function. It is too slow to be practical.
def count_valid_arrangements(towels_trie, trie_branch, design_segment):
    
    if trie_branch == towels_trie and design_segment in arrangement_search_cache:
        return arrangement_search_cache[design_segment]
    else:
        valid_designs_implementations = 0
        # We're at a word finish. If there is no design left, we have a valid arrangement. 
        # If there is design left, we can start searching for a new word starting with what's left of design.
        if trie_branch['word_finished']:
            if not design_segment:
                # Design is exhausted on a word finish marker.  We have a valid arrangement. Return one to increment upstream counter.
                return 1
                # print(f"Found a valid design implementation: {implementation} for {design}")
                # print(f"Running designs count: {valid_designs_implementations}")
            else:
                # There is design left. We can start a new word here, searching from top of trie.
                # Note anything we find and add to total. Cache results.
                search_design_remainder_fresh = count_valid_arrangements(towels_trie, towels_trie, design_segment)
                arrangement_search_cache[design_segment] = search_design_remainder_fresh
                valid_designs_implementations += search_design_remainder_fresh
        if design_segment:
            # There is design left. We can search down trie.
            char = design_segment[0]
            if char in trie_branch['children']:
                continue_search_down_trie = count_valid_arrangements(towels_trie, trie_branch['children'][char], design_segment[1:])
                valid_designs_implementations += continue_search_down_trie
        else:
            return 0
        return valid_designs_implementations

# def count_valid_arrangements(trie, design):
#     trie_branch = trie
#     design_segment = design
#     stack = [(trie_branch, design_segment, [''])]
#     valid_designs_implementations = 0
#     while stack:
#         trie_branch, design_segment, implementation = stack.pop()
#         if trie_branch['word_finished']:
#             if not design_segment:
#                 valid_designs_implementations += 1
#                 print(f"Found a valid design implementation: {implementation} for {design}")
#                 print(f"Running designs count: {valid_designs_implementations}")
#             else:
#                 impl_start_new_word = implementation + ['']
#                 stack.append((trie, design_segment, impl_start_new_word))
#         if design_segment:
#             char = design_segment[0]
#             if char in trie_branch['children']:
#                 implementation[-1] += char
#                 stack.append((trie_branch['children'][char], design_segment[1:], implementation))

#     return valid_designs_implementations     

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        start_time = time.time()
        file_path = sys.argv[1]
        towels, towels_trie, designs = read_towels_info(file_path)
        num_towels = len(towels)
        num_designs = len(designs)
        # print(f"Number of towels: {len(towels)}")
        print(f"Number of designs to check: {len(designs)}")
        # chars_appearing_in_designs = {char for design in designs for char in design}
        # print(f"Chars appearing in designs: {chars_appearing_in_designs}")
        # chars_appearing_in_towels = {char for towel in towels for char in towel}
        # print(f"Chars appearing in towels: {chars_appearing_in_towels}")
        # chars_starting_towels = {towel[0] for towel in towels}
        # print(f"Chars starting towels: {chars_starting_towels}")
        # trie_top_chars = {char for char in towels_trie['children']}
        # print(f"Chars starting trie: {trie_top_chars}")
        
        total_valid_arrangements = 0
        for idx, design in enumerate(designs):
            total_valid_arrangements += count_valid_arrangements(towels_trie, towels_trie, design)
            print(f"Finished design {idx + 1} of {num_designs}. Running total: {total_valid_arrangements}") 

        print(f"Valid design arrangements count:{total_valid_arrangements}")
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time}")
        
        