import pytest
import owlready2

from src.dataclass import Left, Right
from src.engine import OwlEngine
from src.learner import Engine
from src.protocols import *

class TestTeacher:
    def __init__(self, engine: Engine, consepts: List[Consept]):
        self.engine = engine
        self.consepts = consepts
    
    def membership_query(self, axiom: InclutionAxiom) -> bool:
        if len(axiom.left.inf) == 1 and isinstance(axiom.left.inf[0], Consept):
            return self.engine.entails(Left(axiom.left.inf[0], axiom.right))
        
        if len(axiom.right.inf) == 1 and isinstance(axiom.right.inf[0], Consept):
            return self.engine.entails(Right(axiom.left, axiom.right.inf[0]))
        
        raise
    
    def equivalence_query(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        ...
    
    def get_consepts(self) -> List[Consept]:
        return self.consepts