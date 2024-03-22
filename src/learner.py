from src.dataclass import *
from src.protocols import Teacher
from typing import Protocol

class Engine(Protocol):
    """The engine is what the Learner uses to do operations on its hypothosis ontology.
    """
    def entails(self, axiom: Left | Right) -> bool:
        ...
    
    def add_axiom(self, axiom: Left | Right):
        ...
    
    def get_hypothisis(self) -> List[Left | Right]:
        ...

class LearnerImpl:
    def __init__(self, engine: Engine, teacher: Teacher):
        self.engine = engine
        self.teacher = teacher
        
    def run_learner(self) -> List[InclutionAxiom]:
        while True:
            counter_example = self.teacher.equivalence_query(self.get_hypothis())
            if (counter_example == None):
                break
            
            counter_example = self.termenologi_counter_example(counter_example)
            
            if isinstance(counter_example, Right):
                counter_example = self.right_o_essensial(counter_example)
            else:
                counter_example = self.left_o_essensial(counter_example)
            
            self.engine.add_axiom(counter_example)
        return self.get_hypothis()
    
    def get_hypothis(self) -> List[InclutionAxiom]:
        return [a.inclution_axiom() for a in self.engine.get_hypothisis()]
     
    def termenologi_counter_example(self, counter_example: InclutionAxiom) -> Left | Right:
        
        if len(counter_example.right.inf) == 1 and isinstance(counter_example.right.inf[0], Consept):
            return Right(counter_example.right, counter_example.right.inf[0])
        
        if len(counter_example.left.inf) == 1 and isinstance(counter_example.left.inf[0], Consept):
            return Left(counter_example.left.inf[0], counter_example.right)
        
        for n in counter_example.left:
            for c in self.teacher.get_consepts():
                r = Right(n,c)
                if (self.is_counter_example(r)):
                    return r
        
        for n in counter_example.right:
            for c in self.teacher.get_consepts():
                l = Left(c,n)
                if (self.is_counter_example(r)):
                    return l
        raise
            
        
    def is_counter_example(self, axiom: Left | Right) -> bool:
        return (not self.engine.entails(axiom)) and (self.teacher.membership_query(axiom.inclution_axiom()))
    
    
    def right_o_essensial(self, axiom: Right) -> Right:
        ... # TODO
    
    def left_o_essensial(self, axiom: Left) -> Left:
        ... # TODO