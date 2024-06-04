from __future__ import annotations
from dataclasses import dataclass

from typing import List, Dict

from collections import defaultdict

@dataclass
class InclutionAxiom:
    """A general inclution axiom class consisting of a left and right Expression. These are meant as an interface for the learner and teacher to communicate.
    
    example: left ⊑ right (where left and right are Expressions)
    
    example of translations between EL descriptive language and InclutionAxiom:
    
        Mother ⊑ ∃.parent_of.⊤
        
        `InclutionAxiom(left=Expression([Consept("Mother")]), right=Expression([Role("parent_of", Expression([]))]))`
    
    """
    left: Expression
    right: Expression

@dataclass
class Expression:
    """Here, an expression consists of a list of Consepts and Roles. An empty list is treated as ⊤
    
    example: element ⊓ element ⊓ element (where element are different Consepts and Roles)
    
    The class has an iterator goes through the expresson as a tree where each expression is a node and the roles are edges between them.
    It is a breadth-first search algorithm that allows for changing the children of a node as long as you haven't moved pased the node.
    """
    concepts: List[Concept]
    roles: List[Role]
    
    def _group_by_role_name(self, roles: List[Role]) -> Dict[str, List[Role]]:
        grouped = defaultdict(list)
        for item in roles:
            grouped[item.name].append(item)
        return grouped
    
    def __iter__(self):
        return ExpressionIterator(self)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Expression):
            return False
        
        if set(value.concepts) != set(self.concepts):
            return False
        
        if len(value.roles) != len(self.roles):
            return False
        
        # This part is not the best way of doing it, but it works.
        grouped = self._group_by_role_name(value.roles)
        
        for r in self.roles:
            found = False
            l = grouped[r.name]
            for i in l:
                if r.expression == i.expression:
                    found = True
                    break
            if not found:
                return False
        
        return True
    
    
        

class ExpressionIterator:
    """The iterator of an Expression
    """
    def __init__(self, root_expression: Expression):
        self.iter_queue = [root_expression]
        self.current_node = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_queue == None:
            raise StopIteration
        
        if self.current_node != None:
            self.iter_queue.extend(r.expression for r in self.current_node.roles)
        
        if len(self.iter_queue) == 0:
            raise StopIteration
        
        self.current_node = self.iter_queue.pop(0)
        return self.current_node


@dataclass(eq=True, frozen=True)
class Concept:
    """A concept atomic and contains only a name
    
    example: Mother (where Mother is the name)"""
    name: str

@dataclass
class Role:
    """A rol consists of a name and an expression
    
    example: ∃.eats.expression (where eats is the name and expression is an expression)"""
    name: str
    expression: Expression
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Role):
            return False
        
        return value.name == self.name and value.expression == self.expression
