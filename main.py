from typing import *
from trie import Trie
import csv, sys

FrequencyMap = Dict[str, int]


# Execution time: O(n*m + m*|E| + m*lg(m)) < O(n*m + m*lg(m))
# Space: O(n*m)
def heuristic_best_trie(str_list: List[str]) -> Tuple[Trie, int]:
    p = heuristic_best_permutation(str_list)

    permuted_input = (''.join(s[i] for i in p) for s in str_list)   # O(n*m)
    trie = Trie(permuted_input)                                     # O(n*m)
    return trie, trie.nodes()


# Execution time: O(n*m + m + n) ~ O(n*m)
# Space: O(m*|E|)
def heuristic_best_permutation(str_list):            
    dif_count_list = count_different_per_column(str_list)           # O(n * m)
    orig_indexes = map_original_positions(dif_count_list)           # O(m)
    sorted_dif_list = integer_sort(dif_count_list, reverse=False)   # O(m + n)
    return recover_permutation(sorted_dif_list, orig_indexes)       # O(m)


# Execution time: O(n*m), Space: O(m*min(|E|, n)) ~ O(m*|E|)
def count_different_per_column(str_list):
    m = len(str_list[0])
    column_freq: List[FrequencyMap] = [{} for _ in range(m)]        # O(m)
    for string in str_list:                                         # O(n) *
        for index, char in enumerate(string):                       # O(m) *
            if char not in column_freq[index]:                      # |
                column_freq[index][char] = 0                        # O(1)
            column_freq[index][char] += 1                           # |
                                                                    
    return [len(col) for col in column_freq]                        # O(m)


# Execution time: O(m), Space: O(m)
def map_original_positions(col_max_freq):
    # length of col_max_freq is m
    index_map = {}
    for column, frequency in enumerate(col_max_freq):               # O(m) *
        if frequency not in index_map:                              # |
            index_map[frequency] = []                               # O(1)
        index_map[frequency].append(column)                         # |

    return index_map


# Uses counting sort to sort a list of integers.
# Execution time: O(m + n), Space: O(n)
def integer_sort(int_list, reverse=False):
    min_elem, max_elem = min(int_list), max(int_list)
    frequency_list = [0 for _ in range(min_elem, max_elem + 1)]
    sorted_list = []

    for value in int_list:
        frequency_list[value - min_elem] += 1

    for index, count in enumerate(frequency_list):
        real_value = index + min_elem
        sorted_list.extend(iter(real_value for _ in range(count)))

    if reverse is True:
        sorted_list.reverse()

    return sorted_list


# Execution time: O(m), Space: O(m)
def recover_permutation(max_frequencies, original_positions):
    permutation = []
    for frequency in max_frequencies:                               # O(m) *
        position = original_positions[frequency][-1]                # |
        permutation.append(position)                                # O(1)
        original_positions[frequency].pop()                         # |
    return permutation


def main():
    str_list = []
    with open('tests/'+ sys.argv[1] +'.txt', 'r') as file:
        str_list.extend((line.rstrip() for line in file))
    
    if len(str_list) < 1:
        return

    trie = Trie(str_list)

    print("Original:")
    print(f"nodes={trie.nodes()}")
    trie.pretty_print()

    trie2, nodes = heuristic_best_trie(str_list)

    print("Optimized:")
    print(f"{nodes=}")
    trie2.pretty_print()


if __name__ == '__main__':
    main()
