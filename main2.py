from __future__ import annotations
from dataclasses import *
from typing import *
from itertools import groupby
from math import inf

@dataclass
class GenSPT:
    alpha: Optional[int] = None
    children: dict[str, GenSPT] = field(default_factory=dict)

# self descriptive (the behaviour, not the implementation)
def print_tree(root_node: Optional[GenSPT]):
    @dataclass
    class Context:
        root_node: GenSPT
        level: int
        c: str
        children: Optional[Iterator[str, Optional[GenSPT]]] = None
        caller: Optional[Context] = None
        skip_print: bool = False


    self = Context(root_node, 0, "")
    while self is not None:
        if not isinstance(self.root_node, GenSPT):
            print("  " * self.level + self.c + repr(self.root_node))
            self = self.caller
            continue
        
        if not self.skip_print: 
            print("  " * self.level + self.c + f"GenSPT(alpha={self.root_node.alpha}, children=" + "{")
            self.skip_print = True

        if self.children is None: 
            self.children = iter(self.root_node.children.items())

        for char, child in self.children:
            call = Context(child, self.level + 1, char + ": ", caller=self)
            self = call
            break
        else:
            print("  " * self.level + "}")
            self = self.caller

# returns true if all elements in iterable are the same
# complexity O(len(iterable))
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

# returns all equal columns from 0 to m from strings, from row i to j
# Complexity: O((j - i) * m) ~ O(n * m)
def equal_columns(strings, i, j, m):
    def all_eq_in_column(c): 
        return all_equal(strings[x][c] for x in range(i, j))

    return {c for c in range(m) if all_eq_in_column(c)}   

# returns all equal columns from 0 to m from strings, from row i to j
# this version assumes that a column is equal if and only if the first and 
# last chars in the range are equal. This only happens in our case
# Complexity: O(m)
def equal_columns_optimized(strings, i, j, m):
    return {c for c in range(m) if strings[i][c] == strings[j - 1][c]}

# returns an iterable which contains all pairs (x, y) such that 
# strings[c][r] for c in range(x, y) always returns the same value
# Complexity: O((j - i)) ~ O(n)
def subsections(strings, i, j, r):
    for x in range(i + 1, j):
        if strings[x][r] != strings[i][r]:
            yield (i, x)
            i = x
    yield (i, j)


# returns the minimal number of nodes that a GenSPT from strings[i:j] could have
# Complexity: Yes
def OPT(strings, i, j):
    m = len(strings[i])
    # renaming to match with the paper
    K = lambda i, j: equal_columns_optimized(strings, i, j, m) 
    C = lambda i, j, r: subsections(strings, i, j, r)

    def OPT_HAT(i, j):
        if j - i < 2:
            return 0                                                                            
            
        Kij = K(i, j)
        Rij = (x for x in range(m) if x not in Kij)
        # Cijrs = (C(i, j, r) for r in Rij)
        def cost(i_, j_): return OPT_HAT(i_, j_) + len(K(i_, j_)) - len(Kij)

        return min(sum(cost(i_, j_) for i_, j_ in C(i, j, r)) for r in Rij)

    return OPT_HAT(i, j) + len(K(i, j))

def OPT_BUILD(strings, i, j):
    m = len(strings[0])
    K = lambda i, j: equal_columns_optimized(strings, i, j, m)
    C = lambda i, j, r: subsections(strings, i, j, r)
    
    def OPT_BUILD_HAT(i, j):
        if j - i < 2:
            return None, 0

        Kij = K(i, j)
        Rij = (x for x in range(m) if x not in Kij)

        def result_starting_at(r):
            candidate, candidate_edges = GenSPT(r), 0
            for i_, j_ in C(i, j, r):
                tail, tail_edges = OPT_BUILD_HAT(i_, j_)
                Ki_j_ = K(i_, j_)

                for r_ in Ki_j_ - Kij - {r}:
                    tail = GenSPT(r_, {strings[i_][r_]: tail})

                candidate.children[strings[i_][r]] = tail
                candidate_edges += tail_edges + len(Ki_j_) - len(Kij)

            return candidate, candidate_edges

        return min((result_starting_at(row) for row in Rij), key=lambda x: x[1])
        

    Kij = K(i, j)
    root, nodes = OPT_BUILD_HAT(i, j)

    for k_index in Kij:
        root = GenSPT(k_index, {strings[0][k_index]: root})

    return root, (nodes + len(Kij))
    
def OPT_BUILD_CACHED(strings, i, j):
    m = len(strings[0])
    K = lambda i, j: equal_columns_optimized(strings, i, j, m)
    C = lambda i, j, r: subsections(strings, i, j, r)
    
    OPT_BUILD_HAT_CACHE = {}

    def OPT_BUILD_HAT(i, j):
        if (i, j) in OPT_BUILD_HAT_CACHE:
            print('a')
            return OPT_BUILD_HAT_CACHE[(i, j)]

        if j - i < 2:
            print(f"TRIVIAL({i}, {j})")
            return None, 0

        print(f"OPT_BUILD_HAT_CACHED({i}, {j})")
        Kij = K(i, j)
        Rij = (x for x in range(m) if x not in Kij)

        def result_starting_at(r):
            candidate, candidate_edges = GenSPT(r), 0
            for i_, j_ in C(i, j, r):
                tail, tail_edges = OPT_BUILD_HAT(i_, j_)
                Ki_j_ = K(i_, j_)

                for r_ in Ki_j_ - Kij - {r}:
                    tail = GenSPT(r_, {strings[i_][r_]: tail})

                candidate.children[strings[i_][r]] = tail
                candidate_edges += tail_edges + len(Ki_j_) - len(Kij)

            return candidate, candidate_edges

        result = min((result_starting_at(row) for row in Rij), key=lambda x: x[1])
        OPT_BUILD_HAT_CACHE[(i, j)] = result
        return result
        

    Kij = K(i, j)
    root, nodes = OPT_BUILD_HAT(i, j)

    for k_index in Kij:
        root = GenSPT(k_index, {strings[0][k_index]: root})

    return root, (nodes + len(Kij))

def MIN_TRIE_GEN(strings):
    return OPT_BUILD(strings, 0, len(strings))

def MIN_TRIE_GEN_CACHED(strings):
    return OPT_BUILD_CACHED(strings, 0, len(strings))

def main ():
    strings = ['aaaa', 'abbb', 'acbc', 'addd']
    print(OPT(strings, 0, len(strings)))
    

if __name__ == '__main__':
    main()
        