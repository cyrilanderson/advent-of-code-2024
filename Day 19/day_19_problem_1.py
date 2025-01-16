import sys
import re
import time
#import networkx as nx   



# Do this instead with a dictionary
# But also doublecheck my logic with the algo checking the designs


# Adapted from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# Author: Shubhadeep Roychowdhury - https://medium.com/@rcshubha
# class TrieNode(object):
#     """
#     Trie node implementation. Very basic. but does the job
#     """
    
#     def __init__(self, char: str):
#         self.char = char
#         self.children = set()
#         # Is it the last character of the word.`
#         self.word_finished = False
#         # How many times this character appeared in the addition process
#         self.counter = 1
    

#     def add(self, word: str):
#         """
#         Adding a word in the trie structure
#         """
#         node = self
#         for char in word:
#             found_in_child = False
#             # Search for the character in the children of the present `node`
#             for child in node.children:
#                 if child.char == char:
#                     # We found it, increase the counter by 1 to keep track that another
#                     # word has it as well
#                     child.counter += 1
#                     # And point the node to the child that contains this char
#                     node = child
#                     found_in_child = True
#                     break
#             # We did not find it so add a new chlid
#             if not found_in_child:
#                 new_node = TrieNode(char)
#                 node.children.add(new_node)
#                 # And then point node to the new child
#                 node = new_node
#         # Everything finished. Mark it as the end of a word.
#         node.finished_word = True

#     def get_children(self):
#         return self.children
    
#     def get_char(self):
#         return self.char
    
#     def is_finished_word(self):
#         return self.word_finished
    
    
#     def find_prefix(self, prefix: str):
#         """
#         Check and return 
#         1. If the prefix exsists in any of the words we added so far
#         2. If yes then how may words actually have the prefix
#         """
#         node = self
#         # If the root node has no children, then return False.
#         # Because it means we are trying to search in an empty trie
#         if not node.children:
#             return False, 0
#         for char in prefix:
#             char_not_found = True
#             # Search through all the children of the present `node`
#             for child in node.children:
#                 if child.char == char:
#                     # We found the char existing in the child.
#                     char_not_found = False
#                     # Assign node as the child containing the char and break
#                     node = child
#                     break
#             # Return False anyway when we did not find a char.
#             if char_not_found:
#                 return False, 0
#         # Well, we are here means we have found the prefix. Return true to indicate that
#         # And also the counter of the last node. This indicates how many words have this
#         # prefix
#         return True, node.counter



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

    towels = section1.split(', ')
    # print(f"Towel types: {towels}")
    towels_trie = {
            'children': {},
            'word_finished': False,
    }
    current_node = towels_trie
    for towel in towels:
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

# def count_valid_arrangements(towels_trie, design):
#     node = towels_trie
#     remainder_design_validations = []
#     for idx, char in enumerate(design):

#         continue_trie_traversal = False
#         end_of_design = idx == len(design) - 1
#         if char in node['children']:

#             if node['finished_word']:
#                 if end_of_design:
#                     return True
#                 else:
#                     fork_result = validate_design(towels_trie, design[idx+1:])
#                     remainder_design_validations.append(fork_result)               
#             else: 
#                 if end_of_design:
#                     return False
#             if node['children']:
#                 continue_trie_traversal = True
        
#         if not continue_trie_traversal:
#             break # break out of loop over design chars
#         else:
#             node = node['children'][char]

#     if any(remainder_design_validations):
#         return True
#     return False

# Takes in a design string and the towels trie
# Works out how many valid implementations of the design string there are
# using the towel type substrings encoded in the trie
# This will basically use DFS to traverse the trie and the design string
# This could be done recursively, but instead using an iterative version with a stack
# Stack will contain tuples of (trie_branch, design_segment)
def count_valid_arrangements(trie, design):
    trie_branch = trie
    design_segment = design
    stack = [(trie_branch, design_segment)]
    valid_designs_implementations = 0
    while stack:
        trie_branch, design_segment = stack.pop()
        if trie_branch['word_finished']:
            if not design_segment:
                valid_designs_implementations += 1
            else:
                stack.append((trie, design_segment))
        if design_segment:
            char = design_segment[0]
            if char in trie_branch['children']:
                stack.append((trie_branch['children'][char], design_segment[1:]))

    return valid_designs_implementations     

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        start_time = time.time()
        file_path = sys.argv[1]
        towels, towels_trie, designs = read_towels_info(file_path)
        print(f"Number of towels: {len(towels)}")
        print(f"Number of designs: {len(designs)}")
        design_validity_count = 0
        for design in designs:
            result = validate_design(towels_trie, design)
            if result:
                design_validity_count += 1

        print(f"Valid designs: {design_validity_count}")
        end_time = time.time()
        
        
