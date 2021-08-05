from __future__ import annotations
from typing import *
from parsy import *
from dataclasses import * 
from gen_spt import GenSPT

WHITESPACE = regex(r'\s*')
LEXEME = lambda P : P << WHITESPACE

TRIE_DECL = string('GenSPT(')
TRIE_CLOSE = string(')')

def read_str(string):
    remainder = string
    decl, remainder = TRIE_DECL.parse_partial(remainder)


def main():
    print()

if __name__ == '__main__':
    main()


