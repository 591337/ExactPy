from __future__ import annotations
from dataclasses import dataclass

from typing import List, Dict

from collections import defaultdict
"""
These are the data types that the learner and teacher uses when they communicate.
The axioms are build from two trees.

A Node has a list of ConceptExpressions and a list of Edges. Each edge has a Role and a target Node.
"""

@dataclass
class InclusionAxiom:
    """A general inclusion axiom class consisting of a left and right Expression.
    These are meant as an interface for the learner and teacher to communicate.
    
        left ⊑ right
    
    Example:
        Mother ⊑ ∃.parent_of.⊤
        
        ```
        left_node = Node(labels=[ConceptExpression("Mother")], edges=[])
        right_node = Node(labels=[], edges=[Edge(role=Role("parent_of"), target=Node([],[]))])
        
        InclusionAxiom(left=left_node, right=right_node)
        ```
    """
    left: Node
    right: Node

@dataclass
class Node:
    """Here, an expression consists of a list of ConceptExpressions and Edges. If both are empty, the node should be treated as ⊤
    
        concept_expression ⊓ concept_expression ⊓ edge ⊓ edge
    
    example:
        Mother ⊓ Human ⊓ ∃.parent_of.⊤
        
        ```
        mother = ConceptExpression("Mother")
        human = ConceptExpression("Human")
        parent_of = Edge(role=Role("parent_of"), target=Node([],[]))
        
        Node(labels=[mother,human], edges=[parent_of])
        ```
    """
    labels: List[ConceptExpression]
    edges: List[Edge]
    
    def _group_by_role_name(self, edges: List[Edge]) -> Dict[Role, List[Edge]]:
        grouped = defaultdict(list)
        for item in edges:
            grouped[item.label].append(item)
        return grouped
    
    def __iter__(self):
        return NodeIterator(self)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Node):
            return False
        
        if set(value.labels) != set(self.labels):
            return False
        
        if len(value.edges) != len(self.edges):
            return False
        
        # This part is not the best way of doing it, but it works.
        grouped = self._group_by_role_name(value.edges)
        
        for r in self.edges:
            found = False
            l = grouped[r.label]
            for i in l:
                if r.target == i.target:
                    found = True
                    break
            if not found:
                return False
        
        return True
    
    
        

class NodeIterator:
    """    
    The class iterates through the nodes. It uses a breadth-first search algorithm that allows for
    changing the children of a node as long as you haven't moved passed the node.
    """
    def __init__(self, root_expression: Node):
        self.iter_queue = [root_expression]
        self.current_node = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_queue == None:
            raise StopIteration
        
        if self.current_node != None:
            self.iter_queue.extend(r.target for r in self.current_node.edges)
        
        if len(self.iter_queue) == 0:
            raise StopIteration
        
        self.current_node = self.iter_queue.pop(0)
        return self.current_node


@dataclass(eq=True, frozen=True)
class ConceptExpression:
    """A concept expression is an atomic label for the node
    
    example: Mother (where Mother is the name)"""
    name: str

@dataclass(eq=True, frozen=True)
class Role:
    """A role is the name of a edge
    
    example: parent_of"""
    name: str

@dataclass
class Edge:
    """A rol consists of a name and an expression
    
    example: ∃.eats.expression (where eats is the name and expression is an expression)"""
    label: Role
    target: Node
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        
        return value.label == self.label and value.target == self.target
