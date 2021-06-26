from typing import *
from trie import Trie

FrequencyMap = Dict[str, int]


# Execution time: O(n*m + m*|E| + m*lg(m)) < O(n*m + m*lg(m))
# Space: O(n*m)
def heuristic_best_trie(str_list: List[str]) -> Tuple[Trie, int]:
    p = heuristic_best_permutation(str_list)

    permuted_input = (''.join(s[i] for i in p) for s in str_list)  # O(n*m)
    trie = Trie(permuted_input)                                    # O(n*m)
    return trie, trie.nodes()


# Execution time: O(n*m + m*|E| + m*lg(m)) < O(n*m + m*lg(m))
# Space: O(m*|E|)
def heuristic_best_permutation(str_list):
    char_freq_table = char_frequency_table(str_list)  # O(n*m)
    col_max_freq = [max(col.values()) for col in char_freq_table]  # O(m*|E|)
    orig_indexes = original_indexes_per_freq(col_max_freq)  # O(m)
    sorted_frequencies = sorted(col_max_freq, reverse=True)  # O(m*lg(m))
    p = recover_permutation(sorted_frequencies, orig_indexes)  # O(m)
    return p


# Execution time: O(n*m), Space: O(m*min(|E|, n)) ~ O(m*|E|)
def char_frequency_table(str_list):
    m = len(str_list[0])
    column_freq: List[FrequencyMap] = [{} for _ in range(m)]  # O(m)
    for string in str_list:  # O(n) *
        for index, char in enumerate(string):  # O(m) *
            if char not in column_freq[index]:  # |
                column_freq[index][char] = 0  # O(1)
            column_freq[index][char] += 1  # |

    return column_freq


# Execution time: O(m), Space: O(m)
def original_indexes_per_freq(col_max_freq):
    # length of col_max_freq is m
    index_map = {}
    for column, frequency in enumerate(col_max_freq):  # O(m) *
        if frequency not in index_map:  # |
            index_map[frequency] = []  # O(1)
        index_map[frequency].append(column)  # |

    return index_map


# Execution time: O(m), Space: O(m)
def recover_permutation(max_frequencies, original_positions):
    permutation = []
    for frequency in max_frequencies:
        position = original_positions[frequency][-1]
        permutation.append(position)
        original_positions[frequency].pop()
    return permutation


def main():
    str_list = ["aaa",
                "baa",
                "bac",
                "cbb"]

    trie = Trie(str_list)

    trie.pretty_print()
    print(trie.nodes())

    trie2, nodes = heuristic_best_trie(str_list)
    trie2.pretty_print()
    print(nodes)


if __name__ == '__main__':
    main()
