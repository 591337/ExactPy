from typing import List
import pytest

from src.data.special import Right, Left
from src.learner.learner_impl import Engine
from src.data.communication import Concept, InclutionAxiom

class TestTeacher:
    def __init__(self, engine: Engine, concepts: List[Concept]):
        self.engine = engine
        self.concepts = concepts
    
    def membership_query(self, axiom: InclutionAxiom) -> bool:
        if len(axiom.left.concepts) == 1 and len(axiom.left.roles) == 0:
            return self.engine.entails(Right(axiom.left.concepts[0], axiom.right))
        
        if len(axiom.right.concepts) == 1 and len(axiom.right.roles) == 0:
            return self.engine.entails(Left(axiom.left, axiom.right.concepts[0]))
        
        raise ValueError()
    
    def equivalence_query(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        ...
    
    def get_concepts(self) -> List[Concept]:
        return self.concepts