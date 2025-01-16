import sys
import time
# import itertools
# import collections


def read_diskmap(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()
        line = line.strip()
        #print(len(line))
    return line

def expand_diskmap(diskmap):
    # Holds contents of the disk
    contents = []
    # Holds the free space map. Each entry is a tuple representing the index range of the free space
    free_space_map = []
    file_map = []
    # cumulative count of the blocks in the disk
    # blocks numbered from 0 to count - 1
    count = 0
    id = 0
    free = False
    for char in diskmap:
        num = int(char)
        # I have confirmed that there are no 0s in the diskmap for even-numbered indices representing data
        # 0s are only present in the diskmap for odd-numbered indices representing free space
        if not free:
            content_to_add = [id for i in range(num)]
            file_map.append((id, (count, count + num)))
            id += 1
            free = True
        else:
            content_to_add = ['' for i in range(num)]
            free_space_map.append((count, count + num))
            free = False
        contents.extend(content_to_add)
        count += num
    return contents, free_space_map, file_map


def defragment(contents, free_space_map, file_map):
    # rightmost block under consideration
    num_files = len(file_map)
    file_idx = num_files - 1
    while file_idx > 0:
        file_id, file_range = file_map[file_idx]
        file_size = range_capacity(file_range)
        space_idx = 0
        # Can only place file in space to left of file
        # Upper end of space range is less than lower end of file range
        while free_space_map[space_idx][1] <= file_map[file_idx][1][0]:
            # What is the range of space at index space_idx?
            space_range = free_space_map[space_idx]
            # How much space is available in this range? Is it enough to fit the file?
            space_size = range_capacity(space_range)
            if space_size >= file_size:
                space_low, _ = free_space_map[space_idx]
                spaces_used = file_size
                # update contents
                # Enter data from file into the free space
                for i in range(space_low, space_low + spaces_used):
                    contents[i] = file_id
                # Replace file data with empty strings
                for j in range(*file_range):
                    contents[j] = ''
                # update free_space_map at space_idx
                # There may be free space left if the space was larger than the file
                # Otherwise left with empty range
                free_space_map[space_idx] = range_leftover(space_range, spaces_used)
                # update file_map
                # Note if want to keep using file_map afterwards, want to sort it at end by the first element of the tuple
                # Keeping it in place in list for now makes it easier to update the file_map
                file_map[file_idx] = (file_id, (space_low, space_low + spaces_used))
                # We have placed the file, so move to next file
                break
            else:
                space_idx += 1
                continue
        # Try next file to left
        file_idx -= 1
    # sort file map by lower end of range
    file_map.sort(key=lambda x: x[1][0])
    return contents, free_space_map, file_map

def compute_checksum(contents):
    sum = 0
    for idx, num in enumerate(contents):
        if num != '':
            sum += idx * num
    return sum

def find_all_indexes(string, char):
    return [index for index, c in enumerate(string) if c == char]

def range_capacity(range):
    start, end = range
    return end - start

# Given a tuple of two integers representing the lower and upper of a range, 
# and a number of spaces to be taken away, left to right, from the range,
# return the new range after the spaces have been taken away
def range_leftover(range, spaces_used):
    start, end = range
    return (start + spaces_used, end)

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    diskmap = read_diskmap(file_path)
    # print(len(find_all_indexes(diskmap, '0')))
    expanded_diskmap, free_space_map, file_map = expand_diskmap(diskmap)
    # print(len(expanded_diskmap))
    # print(len(free_space_map))
    compressed_diskmap, free_space_map, file_map = defragment(expanded_diskmap, free_space_map, file_map)
    # print(len(compressed_diskmap))
    # print(len(free_space_map))
    # print(compressed_diskmap)
    checksum = compute_checksum(compressed_diskmap)
    print(f"Checksum: {checksum}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_9_problem_1.py <file_path>")
    else:
        main()