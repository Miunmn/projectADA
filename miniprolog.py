from __future__ import annotations
from dataclasses import *
from typing import *

from heuristic import heuristic_best_trie
from gen_spt import GenSPT, print_tree
from prolog_parser import parse_input_file

from functools import reduce
from operator import or_
import sys

#This returns a path to the compiled object.txt
def compile_heuristic(rules, path = '.'):
	tries = {}
	for rule in rules:
		trie, nodes = heuristic_best_trie(rules[rule])
		tries[rule] = trie
	
	with open(f'{path}/object.txt', 'w') as f:
		for t in tries:
			f.write('# ' + t + '\n')
			print(tries[t], file=f)
	
	return path + '/object.txt'

def read_rules(file_name: str):
	with open(file_name, 'r') as file:
		file_content = file.read()
		return parse_input_file(file_content)


def solve_for_x(root: Optional[GenSPT], query: str):
	def find(root: Optional[GenSPT], var: Optional[set]=None):
		if root is None:
			return {var}

		character = query[root.alpha]
		if character == 'X':
			subproblems = (find(c, k) for k, c in root.children.items())
			return reduce(or_, subproblems, set())

		elif character not in root.children:
			return set()

		return find(root.children[character], var)

	return find(root, None)



if __name__ == '__main__':
	file = sys.argv[1]
	rules = read_rules(file)
	filename = compile_heuristic(rules)
	#parser(filename)