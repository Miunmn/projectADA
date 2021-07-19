from math import inf
from typing import *
from dataclasses import dataclass

class Trie:
    EOW: str = '\0'

    def __init__(self):
        self.height: int = 0
        self.children: Dict[Trie] = {}

    def insert(self, string: str):
        return self._insert(self, iter(string))

    def delete(self, string: str):
        return Trie._delete(self, iter(string))

    def insert_all(self, strings: Iterable[str]):
        return sum(1 for string in strings if self.insert(string))

    def delete_all(self, strings: Iterable[str]):
        return sum(1 for string in strings if self.delete(string))

    @staticmethod
    def _insert(self: 'Trie', char_stream: Iterator):
        character = next(char_stream, Trie.EOW)
        success = False
        while character != Trie.EOW:
            s_success, child = self._try_create_child(character)
            success = success or s_success
            self = child
            character = next(char_stream, Trie.EOW)
        return success

    @staticmethod
    def _delete(self: 'Trie', char_stream: Iterator[str]):
        chain: List[Trie] = []
        
        for character in char_stream:
            if character not in self.children: 
                return False
            chain.append((self, character))
            self: Trie = self.children[character]
        
        while len(self.children) == 0:
            self, character = chain[-1]
            chain.pop()
            self.children.pop(character)

        return True

    def _try_create_child(self, char):
        if char in self.children:
            return False, self.children[char]

        new_child: Trie = Trie()
        self.children[char] = new_child
        return True, new_child          

    def __setitem__(self, key: str, value: 'Trie'):
        self._insert(self, (key[c] for c in range(len(key) - 1)))
        cur = self
        for char in key:
            cur.children.setdefault(char, value)
            cur = cur.children[char]



@dataclass(init=False, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class Context:
    this: Trie 
    prefix: str 
    children_keys: Iterable[str]
    child_key: Optional[str]
    count: int 
    caller: 'Context'

    def __init__(self, this: Trie, prefix: str, caller: 'Context' = None):
        self.this: Trie = this
        self.prefix: str = prefix
        self.children_keys: Iterable[str] = iter(this.children.keys())
        self.child_key: Optional[str] = None
        self.count: int = 1
        self.caller: 'Context' = caller


def pretty_print(self: Trie):
    context = Context(self, "")
    while context is not None:
        if len(context.this.children) == 0: 
            context = context.caller
            
        for context.child_key in context.children_keys:
            child: Trie = context.this.children[context.child_key]

            brace = '*--' if context.count == len(context.this.children) else '|--'
            next_lv_brace = "   " if context.count == len(context.this.children) else "|  "

            context.count += 1
            
            print(context.prefix, brace, context.child_key, sep='')
            
            call = Context(child, context.prefix + next_lv_brace, context)
            context = call
            break
        else:
            context = context.caller
            

class GeneralizedSPTrie(Trie):
    pass

n = None
m = None
input_string = []
t = Trie()

#O(n)
def swap(i, j, l, r):
    """
    Swaps columns l and r for all strings
    between and including positions i and j
    """
    for k in range(i, j + 1):
        swap(input_string[k][l], input_string[k][r])

def sweep_equal_front(i, j, p, equal_indexes):
    """
    This function puts all columns with equal values
    between strings i and j after position p-1
    """
    current = p
    for x in equal_indexes:
        swap(i, j, x, current)
        current += 1

#O(n^2)
def K(i, j):
    """
    This function returns the set of indexes
    R so that, for each r in R, all strings
    in the position r are the same character
    """
    indexes = set()
    for r in range(m):
        unique = set()
        for k in range(i, j + 1):
           unique.add(input_string[k][r]) 
        if len(unique) == 1:
            indexes.add(r)
    return indexes

#O(n^2)
def R(i, j):
    """
    This function returns {0...m} \ K
    """
    indexes = {x for x in range(m)}
    return indexes.difference(K(i, j)) 

#O(n)
def C(i, j, r):
    """
    This function returns a set of segments for 
    which, for each segment, the input strings at 
    position r are the same character
    """
    splits = []
    last_pos = i
    for k in range(i + 1, j + 1):
        if input_string[k][r] != input_string[last_pos][r]:
            splits.append((last_pos, k - 1))
            last_pos = k
    if input_string[j][r] == input_string[last_pos][r]:
        splits.append((last_pos, j))
    return splits

def overline_OPT(i, j):
    if i == j:
        return 0
    ans = inf
    for r in R(i, j):
        edge_sum = 0
        #hacer algo al trie
            #mover todos los caracteres de K(i, j) al principio de cada cadena
        for i_hat, j_hat in C(i, j, r):
            edge_sum += overline_OPT(i_hat, j_hat) + len(K(i_hat, j_hat)) - len(K(i, j))
        ans = min(ans, edge_sum)
        #deshacer ese algo al trie
            #volver a poner a su sitio esos caracteres
    return ans

def OPT(i, j):
    return overline_OPT(i, j) + len(K(i, j))

def main():
    global n
    global m
    global input_string
    trie = Trie()
    with open('input.txt', 'r') as file:
        n, m = [int(x) for x in file.readline().split()]
        for string in file.readlines():
            string = string.rstrip('\n')
            input_string.append(string)
            trie.insert(string)
    
    print(OPT(0, 2))
    pretty_print(trie)

    

if __name__ == '__main__':
    main()
        
