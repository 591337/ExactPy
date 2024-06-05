from typing import List
import pytest

from src.data.special import RightTerminology, LeftTerminology
from src.learner.learner_impl import Engine
from src.data.communication import ConceptExpression, InclusionAxiom

class TestTeacher:
    def __init__(self, engine: Engine, concepts: List[ConceptExpression]):
        self.engine = engine
        self.concepts = concepts
    
    def membership_query(self, axiom: InclusionAxiom) -> bool:
        if len(axiom.left.labels) == 1 and len(axiom.left.edges) == 0:
            return self.engine.entails(RightTerminology(axiom.left.labels[0], axiom.right))
        
        if len(axiom.right.labels) == 1 and len(axiom.right.edges) == 0:
            return self.engine.entails(LeftTerminology(axiom.left, axiom.right.labels[0]))
        
        raise ValueError()
    
    def equivalence_query(self, axioms: List[InclusionAxiom]) -> InclusionAxiom | None:
        ...
    
    def get_concepts(self) -> List[ConceptExpression]:
        return self.concepts