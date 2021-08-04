from __future__ import annotations
from dataclasses import *
from typing import *
from main import heuristic_best_trie
from main2 import GenSPT

def write_tree(root_node: Optional[GenSPT], f):
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
            f.write("  " * self.level + self.c + repr(self.root_node) + '\n')
            self = self.caller
            continue
        
        if not self.skip_print: 
            f.write("  " * self.level + self.c + f"GenSPT(alpha={self.root_node.alpha}, children=" + "{\n")
            self.skip_print = True

        if self.children is None: 
            self.children = iter(self.root_node.children.items())

        for char, child in self.children:
            call = Context(child, self.level + 1, char + ": ", caller=self)
            self = call
            break
        else:
            f.write("  " * self.level + "}\n")
            self = self.caller

def heuristic_compilation(rules):
    tries = {}
    for rule in rules:
        T, n = heuristic_best_trie(rules[rule])
        tries[rule] = T
    
    f = open('object.txt', 'w+')
    for t in tries:
        f.write(t + '\n')
        write_tree(tries[t], f)
        f.writelines('#\n')
    f.close()


if __name__ == '__main__':
	with open('tests/test2.txt', 'r') as f:
		buffer = f.read().splitlines()
	#Read
	rules = {}
	for line in buffer:
		preffix = line.split('(')[0]
		characters = line.split('(')[1].rstrip(')').replace(', ', '')
		if rules.get(preffix) is None:
			rules[preffix] = []
		rules[preffix].append(characters)

	heuristic_compilation(rules)

	

		

