from __future__ import annotations
from typing import Protocol
from typing import List

from dataclasses import dataclass

class Learner(Protocol):
    """The learner is the basis of the Angluin's exact learning framework.
    It inteacts with a teacher by sending it queries.
    """
    def runLearner(self) -> List[InclutionAxiom]:
        ...

class Teacher(Protocol):
    """The teacher is who the learner askes questions to in order to learn the ontology
    """
    def membershipQuery(self, axiom: InclutionAxiom) -> bool:
        """Checks if an axiom is the member of the target ontology

        Args:
            axiom (InclutionAxiom): the axiom to check against the ontology

        Returns:
            bool: true if the axiom is a logical consequense of the ontology
        """
        ...
    
    def equivalenceQuery(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        """Checks if an hypothesis ontology is equivalent with the target ontology. It gives
        an counter example if it is not true.

        Args:
            axioms (List[InclutionAxiom]): The hypothesis ontology to be check against the target. 

        Returns:
            InclutionAxiom | None: If it is not a logical consequense, it returns an counter example.
            if it is a logical consequense, it returns None.
        """
        ...
    
    def getConsepts(self) -> List[Consept]:
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
    inf: List[Consept | Role]
    
    def __iter__(self):
        self._iter_queue: List[Expression] = [self]
        return self
    
    def __next__(self) -> Expression:
        if self._iter_queue == None or len(self._iter_queue) == 0:
            raise StopIteration
        
        n = self._iter_queue.pop(0)
        
        self._iter_queue.extend(r.expression for r in n.inf if isinstance(r, Role))
        return n

@dataclass
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
