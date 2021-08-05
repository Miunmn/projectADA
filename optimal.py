from __future__ import annotations
from dataclasses import *
from typing import *
from itertools import groupby
from math import inf

from trie import *

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
# Complexity: (?)
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

        # Complexity: T(j_ - i_) + O(j_ - i_)
        def new_nodes(i_, j_): 
            return OPT_HAT(i_, j_) + len(K(i_, j_)) - len(Kij)
          
        # literally the formula, but cuter (?)
        # Complexity: Idk, u tell me
        return min(sum(new_nodes(i_, j_) for i_, j_ in C(i, j, r)) for r in Rij)

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

        def trie_with_root(r):
            root, edges = GenSPT(r), 0

            for i_, j_ in C(i, j, r):                                          #O(|sigma|)
                branch, branch_edges = OPT_BUILD_HAT(i_, j_)                   
                Ki_j_ = K(i_, j_)
                edges += branch_edges + len(Ki_j_) - len(Kij)

                # append all nodes to the front of the branc (except the root)
                for r_ in Ki_j_ - Kij - {r}:                                   #O(n)
                    branch = GenSPT(r_, {strings[i_][r_]: branch})

                # only then append the branch to the root
                root.children[strings[i_][r]] = branch

            return root, edges

        candidates = (trie_with_root(r) for r in Rij)
        return min(candidates, key=lambda x: x[1])
        

    Kij = K(i, j)
    root, nodes = OPT_BUILD_HAT(i, j)

    # front append, again
    for k_index in Kij:
        root = GenSPT(k_index, {strings[0][k_index]: root})

    return root, (nodes + len(Kij))
    
def OPT_BUILD_CACHED(strings, i, j):
    m = len(strings[0])
    
    K_VALS = {(i, j): equal_columns_optimized(strings, i, j, m) for j in range(len(strings) + 1) for i in range(j)}
    K = lambda i, j: K_VALS[(i, j)]
    C = lambda i, j, r: subsections(strings, i, j, r)
    
    OPT_BUILD_HAT_CACHE = {}

    def OPT_BUILD_HAT(i, j):
        if (i, j) in OPT_BUILD_HAT_CACHE:
            return OPT_BUILD_HAT_CACHE[(i, j)]

        if j - i < 2:
            return None, 0

        Kij = K(i, j)
        Rij = (r for r in range(m) if r not in Kij)

        # Complexity: O(n*(n + m))
        def result_starting_at(r):
            candidate, candidate_edges = GenSPT(r), 0
            for i_, j_ in C(i, j, r):
                # Memo analysis, let's assume the call is free
                tail, tail_edges = OPT_BUILD_HAT(i_, j_)
                Ki_j_ = K(i_, j_)

                # Every r_ can only appear once on the entire tail build
                # O(m) i guess?
                for r_ in Ki_j_ - Kij - {r}:
                    tail = GenSPT(r_, {strings[i_][r_]: tail})

                candidate.children[strings[i_][r]] = tail
                candidate_edges += tail_edges + len(Ki_j_) - len(Kij)

            return candidate, candidate_edges

        result = min((result_starting_at(r) for r in Rij), key=lambda x: x[1])
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

def MIN_TRIE_GEN_DP(strings):
    n = len(strings)
    m = len(strings[0])
    
    #O(m*n^2)
    K_VALS = {(i, j): equal_columns_optimized(strings, i, j, m) for j in range(n + 1) for i in range(j)}
    K = lambda i, j: K_VALS[(i, j)]
    #O(n)
    C = lambda i, j, r: subsections(strings, i, j, r)

    #Initialization: O(n*m)
    OPT_HAT = [[(None, inf)]*(n + 1) for row in range(n)]

    #Base case initialization: O(n)
    for i in range(n):
        OPT_HAT[i][i + 1] = None, 0


    for lenght in range(2, n + 1):                                        #n states
        for i in range(0, n - lenght + 1):                                #O(n)     
            j = i + lenght                                                #O(1) 
            Kij = K(i, j)                                                 #O(1)
            Rij = (r for r in range(m) if r not in Kij)                   #O(1)

            opt, opt_edges = None, inf
            for r in Rij:                                                 #O(m)     
                candidate, candidate_edges = GenSPT(r), 0               
                for i_, j_ in C(i, j, r):                                 #O(|sigma|) ~ O(n) 
                    tail, tail_edges = OPT_HAT[i_][j_]                    #O(1)
                    Ki_j_ = K(i_, j_)                                     #O(1)

                    for r_ in Ki_j_ - Kij - {r}:                          #O(1) amortized (r_ never repeats)
                        tail = GenSPT(r_, {strings[i_][r_]: tail})

                    candidate.children[strings[i_][r]] = tail
                    candidate_edges += tail_edges + len(Ki_j_) - len(Kij) #O(1)

                if candidate_edges < opt_edges:
                    opt, opt_edges = candidate, candidate_edges
            
            OPT_HAT[i][j] = opt, opt_edges
    
    
    Kij = K(0, n)
    root, nodes = OPT_HAT[0][n]

    for k_index in Kij:
        root = GenSPT(k_index, {strings[0][k_index]: root})

    return root, (nodes + len(Kij))

def main ():
    str_list = ['ab', 'bc']

    # with open('tests/build/'+ sys.argv[1] +'.txt', 'r') as file:
    #     str_list.extend((line.rstrip() for line in file))

    trie, nodes = MIN_TRIE_GEN_CACHED(str_list)
    print_tree(trie)
    print(f"{nodes=}")


if __name__ == '__main__':
    main()
        
