from typing import *


# Trie implemented with dicts to reduce the space complexity (no sentinels)
class Trie:
    EOW = '\0'

    def __init__(self, items=None):
        self.children: Dict[str, Trie] = {}
        if items is not None:
            for string in items:
                self.insert(string)

    def insert(self, key: str) -> bool:
        return self._insert(iter(key))

    def pretty_print(self, prefix: str = ""):
        if len(self.children) == 0:
            return

        left_idx = len(self.children)
        for count, (char, child) in enumerate(self.children.items(), 1):
            is_left = (count == left_idx)
            brace = '*--' if is_left else '|--'
            next_lv_brace = "   " if is_left else "|  "

            print(prefix, brace, char, sep='')
            child.pretty_print(prefix + next_lv_brace)

    def values(self):
        if len(self.children) == 0:
            yield ""

        for front_char, child in self.children.items():
            yield from (front_char + rest for rest in child.values())

    def nodes(self):
        if len(self.children) == 0:
            return 0
        return sum(1 + child.nodes() for child in self.children.values())

    def _insert(self, key_chars) -> bool:
        char = next(key_chars, Trie.EOW)
        if char == Trie.EOW:
            return False

        success, child = self._try_create_child(char)
        return child._insert(key_chars) or success

    def _try_create_child(self, char) -> Tuple[bool, 'Trie']:
        if char in self.children:
            return False, self.children[char]
        self.children[char] = new_child = Trie()
        return True, new_child
