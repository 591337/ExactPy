from functools import singledispatch

from typing import List
from typing import Protocol

from dataclass import *
    
class Teacher(Protocol):
    def membershipQuery(self, axiom):
        ...
    
    def equivalenceQuery(self, axioms) -> Axiom | None:
        ...
    
    def getClasses(self) -> List[Class]:
        ...
    

class Engine(Protocol):
    def entails(self, axiom: Axiom) -> bool:
        ...
    
    def addAxiom(self, axiom: Axiom):
        ...
    
    def getHypothisis(self) -> List[Axiom]:
        ...

class Learner:
    
    def __init__(self, engine: Engine, oracle: Teacher, hypothis: List = []):
        self.engine = engine
        self.oracle = oracle
        self.hypothis = hypothis
        
    def termenologiCounterExample(self, counterExample: Axiom) -> Right | Left:
        """
        if len(counterExample.left.inf) == 1 and isinstance(counterExample.left.inf[0], Class):
            return Left(counterExample.left.inf[0], counterExample.right)
        
        if len(counterExample.right.inf) == 1 and isinstance(counterExample.right.inf[0], Class):
            return Right(counterExample.right, counterExample.right.inf[0])
        """
        for n in counterExample.left:
            for c in self.oracle.getClasses():
                r = Left(n,c)
                if (self.isCounterExample(r)):
                    return r
        
        for n in counterExample.right:
            for c in self.oracle.getClasses():
                l = Right(c,n)
                if (self.isCounterExample(r)):
                    return l
        
        raise
            
        
    def isCounterExample(self, axiom: Right | Left):
        return (not self.engine.entails(axiom.node())) and (self.oracle.membershipQuery(axiom.node()))
    
    def runLearner(self):
        while True:
            counterExample = self.oracle.equivalenceQuery(self.hypothis)
            if (counterExample == None):
                return self.hypothis
            
            counterExample = self.termenologiCounterExample(counterExample)
            
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