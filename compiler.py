from optimal import MIN_TRIE_GEN_CACHED, MIN_TRIE_GEN_DP
from heuristic import heuristic_best_trie
from parsy import *
from typing import *
import pickle

import argparse


def dict_from_pairs(pairs: list[tuple[str, str]]):   
    result = dict()
    for key, value in pairs:
        result.setdefault(key, []).append(value)
    return result

WHITESPACE = regex(r'[ ]*')
LEXEME = lambda P: P << WHITESPACE

NAME = LEXEME(regex(r'[A-za-z0-9]+'))
ARGS = LEXEME(letter.at_least(1).concat())
TERMINATOR = string('\n') | eof

RULE = (WHITESPACE >> seq( NAME, ARGS ) << TERMINATOR).map(tuple)
RULES = RULE.at_least(1).map(dict_from_pairs) << WHITESPACE

def encode(rule_dict: dict[str, list[str]], optimal=False):
    encoder = MIN_TRIE_GEN_DP if optimal else heuristic_best_trie

    result = {key: encoder(str_list) for key, str_list in rule_dict.items() }
    for key in result:
        trie, size = result[key]
        print(f"file: {key} generated with {size} nodes")
    return result

def compile_contents (file_contents, output, optimal=False):
    pair_dict = RULES.parse(file_contents)
    encoding = encode(pair_dict, optimal)
    with open(output, 'wb') as out:
        pickle.dump(encoding, out)

def compile_file(file, out, dp=False):
    with open(file, 'r') as f:
        file_contents = f.read()
        compile_contents(file_contents, out, dp)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a miniprolog file.')
    parser.add_argument('file_name', metavar='IN', type=str, 
                        help='path to the input file')

    parser.add_argument('--use-optimal', dest='use_optimal', action='store_const',
                        const=True, default=False,
                        help='sum the integers (default: find the max)')

    parser.add_argument('-output', metavar='OUT', 
                        default='a.out',
                        help='output file from compilation')
    
    namespace = parser.parse_args()
    compile_file(namespace.file_name, namespace.output, namespace.use_optimal)


    