from typing import *
from trie import Trie
import csv, sys

FrequencyMap = Dict[str, int]


# Execution time: O(n*m + m*|E| + m*lg(m)) < O(n*m + m*lg(m))
# Space: O(n*m)
def heuristic_best_trie(str_list: List[str]) -> Tuple[Trie, int]:
    p = heuristic_best_permutation(str_list)

    permuted_input = (''.join(s[i] for i in p) for s in str_list)  # O(n*m)
    trie = Trie(permuted_input)                                    # O(n*m)
    return trie, trie.nodes()


# Execution time: O(n*m + m*|E| + m + n) ~ O(n*m)
# Space: O(m*|E|)
def heuristic_best_permutation(str_list):
    char_freq_table = char_frequency_table(str_list)               # O(n * m)
    col_lens = [len(col) for col in char_freq_table]  # O(m * |E|)
    orig_indexes = original_indexes_per_freq(col_lens)         # O(m)
    sorted_frequencies = integer_sort(col_lens, reverse=False)  # O(m + n)
    p = recover_permutation(sorted_frequencies, orig_indexes)      # O(m)
    return p


# Execution time: O(n*m), Space: O(m*min(|E|, n)) ~ O(m*|E|)
def char_frequency_table(str_list):
    m = len(str_list[0])
    column_freq: List[FrequencyMap] = [{} for _ in range(m)]        # O(m)
    for string in str_list:                                         # O(n) *
        for index, char in enumerate(string):                       # O(m) *
            if char not in column_freq[index]:                      # |
                column_freq[index][char] = 0                        # O(1)
            column_freq[index][char] += 1                           # |

    return column_freq


# Execution time: O(m), Space: O(m)
def original_indexes_per_freq(col_max_freq):
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
    file1 = open('tests/'+ sys.argv[1] +'.txt', 'r')
    Lines = file1.readlines()

    for line in Lines:
        str_list.append(line.strip())

    trie = Trie(str_list)

    trie.pretty_print()
    print(trie.nodes())

    trie2, nodes = heuristic_best_trie(str_list)
    trie2.pretty_print()
    print(nodes)


if __name__ == '__main__':
    main()
