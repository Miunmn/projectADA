from __future__ import annotations
from dataclasses import *
from typing import *
import sys

@dataclass
class GenSPT:
    alpha: Optional[int] = None
    children: dict[str, GenSPT] = field(default_factory=dict)


# self descriptive (the behaviour, not the implementation)
def print_tree(root_node: Optional[GenSPT], file=sys.stdout):
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
        if not issubclass(type(self.root_node), GenSPT):
            print("  " * self.level + self.c + repr(self.root_node), file=file)
            self = self.caller
            continue
        
        if not self.skip_print: 
            print("  " * self.level + self.c + f"GenSPT(alpha={self.root_node.alpha}, children=" + "{", file=file)
            self.skip_print = True

        if self.children is None: 
            self.children = iter(self.root_node.children.items())

        for char, child in self.children:
            call = Context(child, self.level + 1, char + ": ", caller=self)
            self = call
            break
        else:
            print("  " * self.level + "}", file=file)
            self = self.caller
