from parsy import *
from typing import *

WHITESPACE = regex(r'\s*')
LEXEME = lambda P: P << WHITESPACE

LPAREN = LEXEME(string('('))
RPAREN = LEXEME(string(')'))
COMMA  = LEXEME(string(','))
CHARACTER = LEXEME(letter)
RULE_NAME = LEXEME(CHARACTER.at_least(1).concat())

RULE_ARGS = CHARACTER.sep_by(COMMA).concat()
RULE = seq( RULE_NAME, LPAREN >> RULE_ARGS << RPAREN )
RULES = RULE.many()
FILE = whitespace >> RULES

def parse_file (file_contents):
    rules = {}

    parsed = FILE.parse(file_contents)
    for name, value in parsed:
        rules.setdefault(name, []).append(value)

    return rules
    

if __name__ == '__main__':
    file_contents = """
    duenho(a, b)
    duenho(a, c)
    duenho(b, a)
    duenho(c, a)
    duenho(a, d)
    hermanos(a, b, c, d)
    hermanos(a, c, d, a)
    """
    print(parse_file(file_contents))
    
    