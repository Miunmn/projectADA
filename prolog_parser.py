from gen_spt import GenSPT, print_tree
from parsy import *
from typing import *

WHITESPACE = regex(r'\s*')
LEXEME = lambda P: P << WHITESPACE

LPAREN = LEXEME(string('('))
RPAREN = LEXEME(string(')'))
LBRACE = LEXEME(string('{'))
RBRACE = LEXEME(string('}'))
COLON  = LEXEME(string(':'))
SHARP = LEXEME(string('#'))
SQUOTE = LEXEME(string('\''))
DQUOTE = LEXEME(string('"'))
EQ = LEXEME(string('='))

NONE = LEXEME(string('None')).result(None)
NUMBER = LEXEME(regex(r'(0|[1-9][0-9]*)')).map(int)

COMMA  = LEXEME(string(','))
CHARACTER = LEXEME(letter)
NAME = LEXEME(CHARACTER.at_least(1).concat())

ARGS = CHARACTER.sep_by(COMMA).concat()
RULE = seq( NAME, LPAREN >> ARGS << RPAREN )
RULES = RULE.at_least(1)
FILE = whitespace.optional() >> RULES

GEN_SPT_DECL = LEXEME(string('GenSPT'))
GEN_SPT_ALPHA = LEXEME(string('alpha'))
GEN_SPT_CHILDREN = LEXEME(string('children'))

def parse_input_file (file_contents):
    rules = {}

    parsed = FILE.parse(file_contents)
    for name, value in parsed:
        rules.setdefault(name, []).append(value)

    return rules

QUOTED_CHAR = LEXEME(string('\'') >> CHARACTER << string('\''))

@generate
def child_dict_item():
    name = yield QUOTED_CHAR
    yield COLON
    value = yield VALUE
    return name, value

CHILDREN_DICT = LBRACE >> child_dict_item.sep_by(COMMA).map(dict) << RBRACE

TRIE = seq(
    GEN_SPT_DECL >> LPAREN >> 
        GEN_SPT_ALPHA >> EQ >> NUMBER << COMMA,
        GEN_SPT_CHILDREN >> EQ >> CHILDREN_DICT << RPAREN    
).map(lambda x: GenSPT(alpha=x[0], children=x[1]))

VALUE = NONE | TRIE


def parse_trie_file(file_contents):
    return TRIE.parse(file_contents)


if __name__ == '__main__':
    file_contents = "GenSPT(alpha=0, children={'a': GenSPT(alpha=1, children={'d': None}), 'b': GenSPT(alpha=1, children={'a': None}), 'c': GenSPT(alpha=1, children={'a': None})})"
    print(print_tree(parse_trie_file(file_contents)))

    