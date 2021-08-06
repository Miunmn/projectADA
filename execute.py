from __future__ import annotations
from functools import reduce
from operator import or_

from parsy import *
from typing import *

import pickle
import sys

from trie import GenSPT

sys.setrecursionlimit(6000)

WHITESPACE = regex(r'[ ]*')
LEXEME = lambda P: P << WHITESPACE

NAME = LEXEME(regex(r'[A-za-z0-9]+'))
ARGS = LEXEME(letter.at_least(1).concat())
TERMINATOR = string('\n') | eof

QUERY = (WHITESPACE >> seq( NAME, ARGS ) << TERMINATOR).map(tuple)
QUERY_FILE = QUERY.at_least(1) << WHITESPACE


def solve_for_x(root: GenSPT, query: str):
	def find(root: Optional[GenSPT], var: Optional[set]=None):
		if root is None:
			return {var} if var is not None else {}

		character = query[root.alpha]
		if character == 'X':
			subproblems = (find(c, k) for k, c in root.children.items())
			return reduce(or_, subproblems, set())

		elif character not in root.children:
			return set()

		return find(root.children[character], var)

	return find(root, None)


if __name__ == '__main__':
	executable = sys.argv[1]
	query_file = sys.argv[2]

	with open(executable, 'rb') as exe:
		trie_dict = pickle.load(exe)
		with open(query_file, 'r') as qf:
			query_contents = qf.read()
			queries = QUERY_FILE.parse(query_contents)
			for qnum, (name, query) in enumerate(queries, start=1):
				trie, nodes = trie_dict[name] 
				print(f"Query {qnum} -> {solve_for_x(trie, query)}")

