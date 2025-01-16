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
            id += 1
            free = True
        else:
            if num != 0:
                content_to_add = ['' for i in range(num)]
                free_space_map.append((count, count + num))
            else:
                content_to_add = []
            free = False
        contents.extend(content_to_add)
        count += num
    return contents, free_space_map


def compress(contents, free_space_map):
    # rightmost block under consideration
    right = len(contents) - 1
    # loop over free space blocks to fill them with data
    done = False
    for free_space in free_space_map:
        if done:
            break
        start, end = free_space
        for i in range(start, end):
            # if rightmost block is empty, move left until a non-empty block is found
            while contents[right] == '':
                right -= 1
            # swap the non-empty block with the empty block
            if right < i:
                done = True
                break
            contents[i] = contents[right]
            contents[right] = ''
            right -= 1
    free_space_map.clear()
    free_space_map.append((right + 1, len(contents)))
    return contents, free_space_map

def compute_checksum(contents):
    sum = 0
    for idx, num in enumerate(contents):
        if num != '':
            sum += idx * num
        else:
            break
    return sum

def find_all_indexes(string, char):
    return [index for index, c in enumerate(string) if c == char]


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    diskmap = read_diskmap(file_path)
    # print(len(find_all_indexes(diskmap, '0')))
    expanded_diskmap, free_space_map = expand_diskmap(diskmap)
    # print(len(expanded_diskmap))
    # print(len(free_space_map))
    compressed_diskmap, free_space_map = compress(expanded_diskmap, free_space_map)
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