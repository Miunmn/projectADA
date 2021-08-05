from typing import *
import sys

from trie import *
from optimal import subsections


# Execution time: O(n*m)
# Space: O(n*m)
def make_simple_spt(strings: List[str], permutation: List[int]):
    permuted_strings = [''.join(s[i] for i in permutation) for s in strings]
    C = lambda i, j, k: subsections(permuted_strings, i, j, k)

    # any character can only be invoked once in build. 
    # There are n*m characters. Thus, complexity is O(n*m)
    def build(i, j, k):
        if k >= len(permutation):
            return None, 0

        root, edges = GenSPT(permutation[k]), 0
        for i_, j_ in C(i, j, k):
            child, subedges = build(i_, j_, k + 1)
            edges += subedges + 1
            root.children[permuted_strings[i_][k]] = child
        return root, edges

    return build(0, len(permuted_strings), 0)


FrequencyMap = Dict[str, int]

# Execution time: O(n*m + m*|E| + m*lg(m)) < O(n*m + m*lg(m))
# Space: O(n*m)
def heuristic_best_trie(str_list: List[str]):
    p = heuristic_best_permutation(str_list)
    return make_simple_spt(str_list, p)


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

    with open('tests/build/'+ sys.argv[1] +'.txt', 'r') as file:
        str_list.extend((line.rstrip() for line in file))

    trie, nodes = make_simple_spt(str_list, list(range(len(str_list[0]))))

    print(f"Original: nodes={nodes}")
    # print_tree(trie)

    trie2, nodes2 = heuristic_best_trie(str_list)

    print(f"\nOptimized: nodes={nodes2}")
    # print_tree(trie2)


if __name__ == '__main__':
    main()
