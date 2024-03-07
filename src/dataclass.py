from __future__ import annotations
from typing import List

from dataclasses import dataclass


@dataclass
class Node:
    inf: List[Class | Relation]
    
    def __iter__(self):
        self._iter_queue: List[Node] = [self]
        return self
    
    def __next__(self) -> Node:
        if self._iter_queue == None or len(self._iter_queue) == 0:
            raise StopIteration
        
        n = self._iter_queue.pop(0)
        
        self._iter_queue.extend(r.node for r in n.inf if isinstance(r, Relation))
        return n
        

@dataclass
class Class:
    name: str

@dataclass
class Relation:
    name: str
    node: Node

@dataclass
class Axiom:
    left: Node
    right: Node

@dataclass
class Right:
    left: Class
    right: Node
    
    def node(self):
        return Axiom(Node([self.left]), self.right)

@dataclass
class Left:
    left: Node
    right: Class
    
    def node(self):
        return Axiom(self.left, Node([self.right]))
