from __future__ import annotations
from dataclasses import *
from typing import *
from itertools import groupby
from math import inf

@dataclass
class GenSPT:
    alpha: Optional[int] = None
    children: dict[str, GenSPT] = field(default_factory=dict)


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


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
                

def equal_columns(strings, i, j, m):
    def all_eq_in_column(c): 
        return all_equal(strings[x][c] for x in range(i, j))

    return {c for c in range(m) if all_eq_in_column(c)}   


def subsections(strings, i, j, r):
    for x in range(i + 1, j):
        if strings[x][r] != strings[i][r]:
            yield (i, x)
            i = x
    yield (i, j)


def OPT(strings, i, j):
    m = len(strings[i])
    K = lambda i, j: equal_columns(strings, i, j, m)
    C = lambda i, j, r: subsections(strings, i, j, r)

    def OPT_HAT(i, j):
        if j - i < 2:
            return 0

        Kij = K(i, j)
        Rij = (x for x in range(m) if x not in Kij)
        Cijrs = (C(i, j, r) for r in Rij)
        return min(sum(OPT_HAT(ī, j̄) + len(K(ī, j̄)) - len(Kij) for ī, j̄ in Cijr) for Cijr in Cijrs)

    return OPT_HAT(i, j) + len(K(i, j))


def OPT_BUILD(strings, i, j):
    m = len(strings[0])
    K = lambda i, j: equal_columns(strings, i, j, m)
    C = lambda i, j, r: subsections(strings, i, j, r)
    
    OPT_BUILD_HAT_CACHE = {}

    def OPT_BUILD_HAT(i, j):
        if (i, j) in OPT_BUILD_HAT_CACHE:
            return OPT_BUILD_HAT_CACHE[(i, j)]

        if j - i < 2:
            return None, 0

        Kij = K(i, j)
        Rij = (x for x in range(m) if x not in Kij)

        def tree_starting_at_row(r):
            candidate, candidate_edges = GenSPT(r), 0
            for ī, j̄ in C(i, j, r):
                tail, tail_edges = OPT_BUILD_HAT(ī, j̄)
                Kīj̄ = K(ī, j̄)

                for r̄ in Kīj̄ - Kij - {r}:
                    tail = GenSPT(r̄, {strings[ī][r̄]: tail})

                candidate.children[strings[ī][r]] = tail
                candidate_edges += tail_edges + len(Kīj̄) - len(Kij)

            return candidate, candidate_edges

        result = min((tree_starting_at_row(r) for r in Rij), key=lambda x: x[1])
        OPT_BUILD_HAT_CACHE[(i, j)] = result
        return result
        

    Kij = K(i, j)
    root, nodes = OPT_BUILD_HAT(i, j)

    for k_index in Kij:
        root = GenSPT(k_index, {strings[0][k_index]: root})

    return root, (nodes + len(Kij))
    

def MIN_TRIE_GEN(strings):
    return OPT_BUILD(strings, 0, len(strings))

def main ():
    strings = ['aaaa', 'abbb', 'acbc', 'addd']
    build, nodes = MIN_TRIE_GEN(strings)
    print_tree(build)
    print(nodes)
    

if __name__ == '__main__':
    main()
        
