from __future__ import annotations
from dataclasses import *
from typing import *
from heuristic import heuristic_best_trie
from gen_spt import GenSPT, print_tree

#This returns a path to the compiled object.txt
def heuristic_compilation(rules, path = ''):
    tries = {}
    for rule in rules:
        T, n = heuristic_best_trie(rules[rule])
        tries[rule] = T
    
    f = open(path + '/object.txt', 'w+')
    for t in tries:
        f.write(t + '\n')
        print_tree(tries[t], file=f)
        f.writelines('#\n')
	f.close()
	
	return path + '/object.txt'

def read_rules():
	with open('tests/queries_1.txt', 'r') as f:
		buffer = f.read().splitlines()
	for line in buffer:
		preffix = line.split('(')[0]
		characters = line.split('(')[1].rstrip(')').replace(', ', '')
		if rules.get(preffix) is None:
			rules[preffix] = []
		rules[preffix].append(characters)

def read_queries(path = ''):
	pass

#For now it receives "tries", but it has to read it
def parser(tries):
	#Read tries: TODO
	#Read queries
	rules = read_queries()
	#Process queries: match each query to each trie
	# - This seems to be just locating the right branch for each query
	#Print results

if __name__ == '__main__':
	rules = read_rules()
	filename = heuristic_compilation(rules)
	#parser(filename)