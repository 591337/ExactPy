from __future__ import annotations
from typing import Protocol, Set
from typing import List

from dataclasses import dataclass

class Learner(Protocol):
    """The learner is the basis of the Angluin's exact learning framework.
    It inteacts with a teacher by sending it queries.
    """
    def run_learner(self) -> List[InclutionAxiom]:
        ...

class Teacher(Protocol):
    """The teacher is who the learner askes questions to in order to learn the ontology
    """
    def membership_query(self, axiom: InclutionAxiom) -> bool:
        """Checks if an axiom is the member of the target ontology

        Args:
            axiom (InclutionAxiom): the axiom to check against the ontology

        Returns:
            bool: true if the axiom is a logical consequense of the ontology
        """
        ...
    
    def equivalence_query(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        """Checks if an hypothesis ontology is equivalent with the target ontology. It gives
        an counter example if it is not true.

        Args:
            axioms (List[InclutionAxiom]): The hypothesis ontology to be check against the target. 

        Returns:
            InclutionAxiom | None: If it is not a logical consequense, it returns an counter example.
            if it is a logical consequense, it returns None.
        """
        ...
    
    def get_consepts(self) -> List[Consept]:
        """The learner is responsible to know what Consepts and Roles the ontology consists of.

        Returns:
            List[Consept]: The consepts of the ontology.
        """
        ...

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
    """
    consepts: List[Consept]
    roles: List[Role]
    
    def __iter__(self):
        return ExpressionIterator(self)

class ExpressionIterator:
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
class Consept:
    """A consept atomic and contains only a name
    
    example: Mother (where Mother is the name)"""
    name: str

@dataclass
class Role:
    """A rol consists of a name and an expression
    
    example: ∃.eats.expression (where eats is the name and expression is an expression)"""
    name: str
    expression: Expression
