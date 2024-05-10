from __future__ import annotations

from src.dataclass import Right, Left
from src.protocols import Teacher, InclutionAxiom, Expression, Consept, Role
from typing import Protocol, List
import copy

class Engine(Protocol):
    """The engine is what the Learner uses to do operations on its hypothosis ontology.
    """
    def entails(self, axiom: Right | Left | InclutionAxiom) -> bool:
        ...
    
    def add_axiom(self, axiom: Right | Left):
        ...
    
    def get_hypothisis(self) -> List[Right | Left]:
        ...

class LearnerImpl:
    def __init__(self, engine: Engine, teacher: Teacher):
        self.engine = engine
        self.teacher = teacher
        
    def run_learner(self) -> List[InclutionAxiom]:
        while True:
            counter_example = self.teacher.equivalence_query(self._get_hypothis())
            if (counter_example == None):
                break
            
            counter_example = self._termenologi_counter_example(counter_example)
            
            if isinstance(counter_example, Right):
                counter_example = self.right_o_essensial(counter_example)
            else:
                counter_example = self.left_o_essensial(counter_example)
            
            self.engine.add_axiom(counter_example)
        return self._get_hypothis()
    
    def _get_hypothis(self) -> List[InclutionAxiom]:
        return [a.inclution_axiom() for a in self.engine.get_hypothisis()]
    
    def _is_consept(self, expression: Expression) -> bool:
        return len(expression.consepts) == 0 and len(expression.roles) == 0
    
    def _termenologi_counter_example(self, counter_example: InclutionAxiom) -> Right | Left:
        
        if self._is_consept(counter_example.right):
            return Left(counter_example.left, counter_example.right.consepts[0])
        
        if self._is_consept(counter_example.left):
            return Right(counter_example.left.consepts[0], counter_example.right)
        
        for n in counter_example.left:
            for c in self.teacher.get_consepts():
                l = Left(n,c)
                if (self._is_counter_example(l)):
                    return l
        
        for n in counter_example.right:
            for c in self.teacher.get_consepts():
                r = Right(c,n)
                if (self._is_counter_example(r)):
                    return r
        
        raise ValueError("Counter example could not be made into a ")
            
        
    def _is_counter_example(self, axiom: Right | Left) -> bool:
        return (not self.engine.entails(axiom)) and (self.teacher.membership_query(axiom.inclution_axiom()))
    
    
    def right_o_essensial(self, axiom: Right) -> Right:
        ... # TODO
    
    def left_o_essensial(self, axiom: Left) -> Left:
        ... # TODO
    
    def saturate_right(self, axiom: Right) -> Right:
        root = True
        for e in axiom.right:
            for c in self.teacher.get_consepts():
                if (root and c == axiom.left) or c in e.consepts:
                    continue
                e.consepts.append(c)
                if not self._is_counter_example(axiom):
                    e.consepts.pop()
            root = False
        return axiom
    
    def saturate_left(self, axiom: Left) -> Left:
        org_express = copy.deepcopy(axiom.left)
        
        root = True
        for e in axiom.left:
            for c in self.teacher.get_consepts():
                if (root and c == axiom.right) or c in e.consepts:
                    continue
                e.consepts.append(c)
                if not self.engine.entails(InclutionAxiom(org_express, axiom.left)):
                    e.consepts.pop()
                else:
                    org_express = copy.deepcopy(axiom.left)
            root = False
        return axiom
    
    def decompose_right(self, right: Right) -> Right:
        axiom = right
        root = True
        
        for n in axiom.right:
            for c in n.consepts:
                if (root and c == right.left):
                    continue
                
                for i in range(len(n.roles)-1, -1, -1):
                    r = n.roles[i]
                    a = Right(c, Expression([], [r]))
                    
                    if self.teacher.membership_query(a.inclution_axiom()):
                        if self.engine.entails(a):
                            n.roles.pop(i)
                        else:
                            return self.decompose_right(a)
            
            root = False
        
        return axiom
    
    
    def decompose_left(self, left: Left) -> Left:
        axiom = left
        root = True
        
        for n in axiom.left:
            if not root:
                for c in self.teacher.get_consepts():
                    a = Left(n, c)
                    if self._is_counter_example(a):
                        return self.decompose_left(a)
            
            for i in range(len(n.roles)):
                roles_copy = n.roles.copy()
                n.roles.pop(i)
                for c in self.teacher.get_consepts():
                    a = Left(axiom.left, c)
                    if self._is_counter_example(a):
                        axiom.right = c
                        roles_copy = n.roles.copy()
                    else:
                        n.roles = roles_copy
            
            root = False
        
        return left
    
    def sibling_merge(self, axiom: Right) -> Right:
        exp = axiom.right
        
        for n in exp:
            roles = n.roles
            for i in range(len(roles)-2,-1,-1):
                for j in range(len(roles)-1,i,-1):
                    if (roles[i].name != roles[j].name):
                        continue
                    new_roles = roles.copy()
                    new_role = Role(roles[i].name, self.expression_merge(roles[i].expression, roles[j].expression))
                    new_roles.pop(j)
                    new_roles[i] = new_role
                    
                    n.roles = new_roles
                    
                    if self.teacher.membership_query(axiom.inclution_axiom()):
                        roles = new_roles
                    else:
                        n.roles = roles
                    
        return axiom
                    

    def expression_merge(self, exp1: Expression, exp2: Expression) -> Expression:
        consepts = exp1.consepts.copy()
        for c in exp2.consepts:
            if c not in consepts:
                consepts.append(c)
        
        roles = exp1.roles.copy()
        roles.extend(exp2.roles)
        
        return Expression(consepts, roles)
        
        