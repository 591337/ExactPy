from __future__ import annotations

from src.data.special import RightTerminology, LeftTerminology
from src.data.communication import InclusionAxiom, Node, ConceptExpression, Edge
from src.teacher.teacher import Teacher
from typing import List
import copy

from src.engine.engine import Engine

class LearnerImpl:
    """Implementation of the learner. This onn based on the Angluin's exact learning framework.
    """
    def __init__(self, engine: Engine, teacher: Teacher):
        self.engine = engine
        self.teacher = teacher
        
    def run_learner(self) -> List[InclusionAxiom]:
        """Starts running the learner. It uses the given teacher as its teacher.

        Returns:
            List[InclusionAxiom]: Returns the discovered ontology as a list of InclusionAxioms
        """
        
        # This loops repeats until the teacher does not give back a counterexample
        while True:
            counter_example = self.teacher.equivalence_query(self._get_hypothesis())
            if (counter_example == None):
                break
            
            # After getting a counterexample, the example is tuned into a terminology
            counter_example = self._terminology_counter_example(counter_example)
            
            if isinstance(counter_example, RightTerminology):
                counter_example = self.right_o_essential(counter_example)
            else:
                counter_example = self.left_o_essential(counter_example)
            
            self.engine.add_axiom(counter_example)
        return self._get_hypothesis()
    
    def _get_hypothesis(self) -> List[InclusionAxiom]:
        """Gets the hypothesis ontology from the engine

        Returns:
            List[InclusionAxiom]: The hypothesis ontology
        """
        return [a.inclusion_axiom() for a in self.engine.get_hypothesis()]
    
    def _is_concept(self, expression: Node) -> bool:
        """Checks if an expression is a concept expression

        Args:
            expression (Node): node input

        Returns:
            bool: returns true if the node consists of only one label
        """
        return len(expression.labels) == 1 and len(expression.edges) == 0
    
    def _terminology_counter_example(self, counter_example: InclusionAxiom) -> RightTerminology | LeftTerminology:
        """Turning the counter example into a terminology.

        Args:
            counter_example (InclusionAxiom): Counter example

        Raises:
            ValueError: If it can not turn it into a terminology, an error is rased

        Returns:
            RightTerminology | LeftTerminology: The counter example in the form of a terminology.
        """
        
        # If one of the sides only consists of a concept expression, it is already a terminology
        if self._is_concept(counter_example.left):
            return RightTerminology(counter_example.left.labels[0], counter_example.right)
        
        if self._is_concept(counter_example.right):
            return LeftTerminology(counter_example.left, counter_example.right.labels[0])
        
        # Naively trying to construct a terminology 
        for n in counter_example.right:
            for c in self.teacher.get_concepts():
                r = RightTerminology(c,n)
                if (self._is_counter_example(r)):
                    return r
        
        for n in counter_example.left:
            for c in self.teacher.get_concepts():
                l = LeftTerminology(n,c)
                if (self._is_counter_example(l)):
                    return l
        
        raise ValueError("Counter example could not be made into a terminology")
            
        
    def _is_counter_example(self, axiom: RightTerminology | LeftTerminology) -> bool:
        """Checks if the terminology is still a counter example.

        Args:
            axiom (RightTerminology | LeftTerminology): Terminology

        Returns:
            bool: returns true if it does not entail from the current hypothesis, 
                  but is still a logical consequence of the target ontology
        """
        return (not self.engine.entails(axiom)) and (self.teacher.membership_query(axiom.inclusion_axiom()))
    
    
    def right_o_essential(self, axiom: RightTerminology) -> RightTerminology:
        """Returns the right_o_essential of the terminology

        Args:
            axiom (RightTerminology): counter example as terminology

        Returns:
            RightTerminology: right_o_essential
        """
        axiom = self._right_o_essential(axiom)
        
        # If there already is a terminology with the same concept expression on the left
        # the two gets merged before finding the right_o_essential again.
        hyp = self.engine.get_right_from_hypothesis(axiom.left)
        if hyp != None:
            expr = axiom.right
            for c in hyp.right.labels:
                if c not in expr.labels:
                    expr.labels.append(c)
            
            expr.edges.extend(hyp.right.edges)
            
            axiom = self._right_o_essential(axiom)
        
        return axiom
        
    
    def _right_o_essential(self, axiom: RightTerminology) -> RightTerminology:
        axiom = self.decompose_right(axiom)
        axiom = self.saturate_right(axiom)
        axiom = self.decompose_right(axiom)
        axiom = self.sibling_merge(axiom)
        
        return axiom
    
    def left_o_essential(self, axiom: LeftTerminology) -> LeftTerminology:
        axiom = self.decompose_left(axiom)
        axiom = self.saturate_left(axiom)
        
        return axiom
    
    def saturate_right(self, axiom: RightTerminology) -> RightTerminology:
        root = True
        for e in axiom.right:
            for c in self.teacher.get_concepts():
                if (root and c == axiom.left) or c in e.labels:
                    continue
                e.labels.append(c)
                if not self._is_counter_example(axiom):
                    e.labels.pop()
            root = False
        return axiom
    
    def saturate_left(self, axiom: LeftTerminology) -> LeftTerminology:
        org_express = copy.deepcopy(axiom.left)
        
        root = True
        for e in axiom.left:
            for c in self.teacher.get_concepts():
                if (root and c == axiom.right) or c in e.labels:
                    continue
                e.labels.append(c)
                if not self.engine.entails(InclusionAxiom(org_express, axiom.left)):
                    e.labels.pop()
                else:
                    org_express = copy.deepcopy(axiom.left)
            root = False
        return axiom
    
    def decompose_right(self, right: RightTerminology) -> RightTerminology:
        axiom = right
        root = True
        
        for n in axiom.right:
            for c in n.labels:
                if (root and c == right.left):
                    continue
                
                for i in range(len(n.edges)-1, -1, -1):
                    r = n.edges[i]
                    a = RightTerminology(c, Node([], [r]))
                    
                    if self.teacher.membership_query(a.inclusion_axiom()):
                        if self.engine.entails(a):
                            n.edges.pop(i)
                        else:
                            return self.decompose_right(a)
            
            root = False
        
        return axiom
    
    
    def decompose_left(self, left: LeftTerminology) -> LeftTerminology:
        axiom = left
        root = True
        
        for n in axiom.left:
            if not root:
                for c in self.teacher.get_concepts():
                    a = LeftTerminology(n, c)
                    if self._is_counter_example(a):
                        return self.decompose_left(a)
            
            for i in range(len(n.edges)):
                roles_copy = n.edges.copy()
                n.edges.pop(i)
                found = False
                for c in self.teacher.get_concepts():
                    a = LeftTerminology(axiom.left, c)
                    if self._is_counter_example(a):
                        axiom.right = c
                        roles_copy = n.edges.copy()
                        found = True
                        break
                if not found:
                    n.edges = roles_copy
            
            root = False
        
        return left
    
    def sibling_merge(self, axiom: RightTerminology) -> RightTerminology:
        exp = axiom.right
        
        for n in exp:
            roles = n.edges
            for i in range(len(roles)-2,-1,-1):
                for j in range(len(roles)-1,i,-1):
                    if (roles[i].label != roles[j].label):
                        continue
                    new_roles = roles.copy()
                    new_role = Edge(roles[i].label, self.expression_merge(roles[i].target, roles[j].target))
                    new_roles.pop(j)
                    new_roles[i] = new_role
                    
                    n.edges = new_roles
                    
                    if self.teacher.membership_query(axiom.inclusion_axiom()):
                        roles = new_roles
                    else:
                        n.edges = roles
                    
        return axiom
                    

    def expression_merge(self, exp1: Node, exp2: Node) -> Node:
        concepts = exp1.labels.copy()
        for c in exp2.labels:
            if c not in concepts:
                concepts.append(c)
        
        roles = exp1.edges.copy()
        roles.extend(exp2.edges)
        
        return Node(concepts, roles)
        
        