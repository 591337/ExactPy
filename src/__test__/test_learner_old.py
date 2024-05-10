from src.__test__.expression_parser import expr
from src.protocols import Consept, InclutionAxiom
import pytest
import owlready2

from src.__test__.expression_parser import expr
from src.dataclass import Right, Left
from src.engine import OwlEngine

from src.__test__.teacher_mock import TestTeacher

from src.learner import LearnerImpl

from src.protocols import Consept

def test_saturate_left():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("A"), Consept("B"), Consept("C"), Consept("D"), Consept("E"), Consept("F")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = InclutionAxiom(expr("A","B","C"), expr("D","E","F"))
    ## teacher_engine.add_axiom(axiom)
    # TODO: Need to change the add_axiom thing so that it accepts non termenologies
    
    