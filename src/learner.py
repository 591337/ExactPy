from dataclass import *
from protocols import Teacher
from typing import Protocol

class Engine(Protocol):
    """The engine is what the Learner uses to do operations on its hypothosis ontology.
    """
    def entails(self, axiom: InclutionAxiom) -> bool:
        ...
    
    def addAxiom(self, axiom: InclutionAxiom):
        ...
    
    def getHypothisis(self) -> List[InclutionAxiom]:
        ...

class Learner:
    
    def __init__(self, engine: Engine, oracle: Teacher):
        self.engine = engine
        self.oracle = oracle
        
    def termenologiCounterExample(self, counterExample: InclutionAxiom) -> Right | Left:
        """
        if len(counterExample.left.inf) == 1 and isinstance(counterExample.left.inf[0], Class):
            return Left(counterExample.left.inf[0], counterExample.right)
        
        if len(counterExample.right.inf) == 1 and isinstance(counterExample.right.inf[0], Class):
            return Right(counterExample.right, counterExample.right.inf[0])
        """
        for n in counterExample.left:
            for c in self.oracle.getConsepts():
                r = Left(n,c)
                if (self.isCounterExample(r)):
                    return r
        
        for n in counterExample.right:
            for c in self.oracle.getConsepts():
                l = Right(c,n)
                if (self.isCounterExample(r)):
                    return l
        
        raise
            
        
    def isCounterExample(self, axiom: Right | Left):
        return (not self.engine.entails(axiom.inclutionAxiom())) and (self.oracle.membershipQuery(axiom.inclutionAxiom()))
    
    def runLearner(self) -> List[InclutionAxiom]:
        while True:
            hypothisis = self.engine.getHypothisis()
            counterExample = self.oracle.equivalenceQuery(hypothisis)
            if (counterExample == None):
                return hypothisis
            
            counterExample = self.termenologiCounterExample(counterExample)
            """
            counterExample = self.computeEssentialCounterexample(counterExample)
        
    @singledispatch    
    def computeEssentialCounterexample(self, counterExample: Right | Left):
        print("using default")
        
    @computeEssentialCounterexample.register
    def _(self, counterExample: Right):
        print("using left")
        
    @computeEssentialCounterexample.register
    def _(self, counterExample: Left):
        print("using left")
"""
