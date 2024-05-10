from typing import List
import pytest

from src.dataclass import Right, Left
from src.learner import Engine
from src.protocols import Consept, InclutionAxiom

class TestTeacher:
    def __init__(self, engine: Engine, consepts: List[Consept]):
        self.engine = engine
        self.consepts = consepts
    
    def membership_query(self, axiom: InclutionAxiom) -> bool:
        if len(axiom.left.consepts) == 1 and len(axiom.left.roles) == 0:
            return self.engine.entails(Right(axiom.left.consepts[0], axiom.right))
        
        if len(axiom.right.consepts) == 1 and len(axiom.right.roles) == 0:
            return self.engine.entails(Left(axiom.left, axiom.right.consepts[0]))
        
        raise ValueError()
    
    def equivalence_query(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        ...
    
    def get_consepts(self) -> List[Consept]:
        return self.consepts