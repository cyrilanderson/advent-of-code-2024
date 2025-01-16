import sys
import re
import time
#import networkx as nx   



# Do this instead with a dictionary
# But also doublecheck my logic with the algo checking the designs


# Adapted from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# Author: Shubhadeep Roychowdhury - https://medium.com/@rcshubha
class TrieNode(object):
    """
    Trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = set()
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

    def add(self, word: str):
        """
        Adding a word in the trie structure
        """
        node = self
        for char in word:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.add(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.finished_word = True

    def get_children(self):
        return self.children
    
    def get_char(self):
        return self.char
    
    def is_finished_word(self):
        return self.word_finished
    
    
    def find_prefix(self, prefix: str):
        """
        Check and return 
        1. If the prefix exsists in any of the words we added so far
        2. If yes then how may words actually have the prefix
        """
        node = self
        # If the root node has no children, then return False.
        # Because it means we are trying to search in an empty trie
        if not node.children:
            return False, 0
        for char in prefix:
            char_not_found = True
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    char_not_found = False
                    # Assign node as the child containing the char and break
                    node = child
                    break
            # Return False anyway when we did not find a char.
            if char_not_found:
                return False, 0
        # Well, we are here means we have found the prefix. Return true to indicate that
        # And also the counter of the last node. This indicates how many words have this
        # prefix
        return True, node.counter



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
    towels_trie = TrieNode('*')
    for towel in towels:
        towels_trie.add(towel)
        print(towels_trie.find_prefix(towel))

    return towels, towels_trie, designs

def validate_design(towels_trie, design):
    node = towels_trie
    remainder_design_validations = []
    for idx, char in enumerate(design):
        # We don't keep going after this character in design unless 
        # (1) We find a match for this char in the children of the current node
        # (2) There are more children to continue traversing the trie
        # So set the flag False before char loop
        continue_trie_traversal = False
        # Need to check each char if it's the last. Have to handle differently if it's the end of the design
        end_of_design = idx == len(design) - 1
        for child in node.get_children():
            # First we need to see if the char matches any of the children. If it does, then we can continue traversing the trie
            if child.get_char() == char:
                node = child
                # Did you reach a finished word? 
                # Note that because of how tries work, this can be at bottom of trie or in the middle of the traversal
                if node.is_finished_word():
                    # If there is design remaining, you can validate that as a design. Otherwise you're done. Success. 
                    # This is the base case. You finish the design on a word.
                    if end_of_design:
                        return True
                    # You're at the end of a word, but there some design remainder left that could be 
                    # searched as its own design.
                    else:
                        # You're in the middle of the design and you've hit a completed word.
                        # Valdiate the remainder of the design as a design
                        fork_result = validate_design(towels_trie, design[idx+1:])
                        # add the alternate path to the list of completed words
                        # You might encounter multiple complete words en route to traversing to bottom of trie.
                        # For carton, you might find car, cart, and carton. All on same path of traversal.
                        # So have to keep track of all the completed words
                        remainder_design_validations.append(fork_result)
                        
                else: 
                    # You have a char match. The bottom of the trie is always a finished word.
                    # You can't reach the bottom and not be on a finished word.
                    # But the word is not finished. So you can't be at the bottom of the trie here. So normally you should keep traversing the trie
                    # to either reach the bottom or finish a word.
                    # But what if the design is finished already? Then the design is not valid, or rather this branch of trying to 
                    # represent the design in words is not successful. Because a design has to finish on a word
                    if end_of_design:
                        return False
                # You have a char match. And you're not at the end of the design. Otherwise would already have returned above
                # So you can continue traversing the trie and comparing, whether you found a word above or not, if there is trie left to traverse.
                # Is there? Does the current node have children?.
                if node.get_children():
                    continue_trie_traversal = True
                # Note. Don't need to consider else here. If there are no children, we're at the bottom of the trie
                # And that means the char match would have been a finished word and already dealt with above
                
                # char match so don't need to check other children
                # break out of loop over children
                break # break out of loop over children
        
        # Before we head to check the next char in the design check if continue has been flagged False
        # Due to reaching the bottom of the trie traversal
        # If it's false, stop checking the rest of the design. The rest of the design for each found word
        # being checked on another stack frame 

        # What about the case where you loop over all the children and none of them match the char?
        # Have I captured that case? I think I have. Because if you loop over all the children and none of them match   
        # the char, then you don't set continue_trie_traversal to True. So it remains False.
        if not continue_trie_traversal:
            # You don't necessarily have to return False here. If you 
            break # break out of loop over design chars
        # Otherwise you continue to the next char in the design
    
    # Suppose the first char in the design is not in the first chars in the trie. You would not continue the trie traversal
    # You would break out of the loop over the design chars. So you would reach this point.

    # Alternatively, you could reach here if you found a word above along the way but then something failed afterwards
    # For example, car was a valid word matching design, but then cart or carton do not match the design
    # So you have to check if there are any remainder design validations done, and if any of them succeeded
    
    if remainder_design_validations:
        if any(remainder_design_validations):
            return True
    # The previous check covers the case where you hit a completed word somewhere along the traversal of the trie
    # If none of those were successful when validating what was left of the design, then not valid
    # No harm to leave this but think about whether it's redundant. Are there any cases that get past the previous checks?
    return False

        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        start_time = time.time()
        file_path = sys.argv[1]
        towels, towels_trie, designs = read_towels_info(file_path)
        # design_validity_count = 0
        # for design in designs:
        #     result = validate_design(towels_trie, design)
        #     if result:
        #         design_validity_count += 1

        # print(f"Valid designs: {design_validity_count}")
        end_time = time.time()
        
        
