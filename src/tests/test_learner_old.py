from src.tests.expression_parser import expr
from src.data.communication import ConceptExpression
import pytest
import owlready2

from src.tests.expression_parser import expr
from src.data.special import RightTerminology, LeftTerminology
from src.engine.engine_impl import OwlEngine

from src.tests.teacher_mock import TestTeacher

from src.learner.learner_impl import LearnerImpl

def test_sibling_merge():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("A"), ConceptExpression("B"), ConceptExpression("C")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    merged_axiom = RightTerminology(ConceptExpression("A"), expr({"r": ["C","B"]}, {"r": ["A"]}))
    teacher.engine.add_axiom(merged_axiom)
    
    axiom = RightTerminology(ConceptExpression("A"), expr({"r": ["C"]}, {"r": ["B"]}, {"r": ["A"]}))
    
    merged = learner.sibling_merge(axiom)
    
    assert merged_axiom == merged

# unsaturate_left

def test_decompose():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, 
        [ConceptExpression("G"), ConceptExpression("H"), ConceptExpression("A"), 
         ConceptExpression("B"), ConceptExpression("C"), ConceptExpression("E"), 
         ConceptExpression("F"), ConceptExpression("D"), 
         ])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = LeftTerminology(expr("A", {"r": ["B"]}), ConceptExpression("C"))
    teacher_engine.add_axiom(axiom)
    axiom = RightTerminology(ConceptExpression("B"), expr("D", "E"))
    teacher_engine.add_axiom(axiom)
    
    axiom = RightTerminology(ConceptExpression("E"), expr("F", {"r": ["G"]}))
    teacher_engine.add_axiom(axiom)
    axiom = RightTerminology(ConceptExpression("H"), expr("G"))
    teacher_engine.add_axiom(axiom)
    
    axiom = LeftTerminology(expr("A", {"r": ["B"]}), ConceptExpression("C"))
    decomposed = learner.decompose_left(axiom)
    assert decomposed == LeftTerminology(expr("B"), ConceptExpression("E"))
    
    axiom = RightTerminology(ConceptExpression("E"), expr("F", {"r": ["G"]}))
    decomposed = learner.decompose_right(axiom)
    # TODO: Not the same as the original one
    # assert decomposed == Right(Concept("H"), expr("G"))

def test_saturate_with_tree_right():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, 
        [ConceptExpression("A"), ConceptExpression("B"), ConceptExpression("C"), 
         ConceptExpression("D"), ConceptExpression("E"), ConceptExpression("F")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    l = LeftTerminology(expr("A", "B", "C"), ConceptExpression("Something"))
    r = RightTerminology(ConceptExpression("Something"), expr("D", "E", "F"))
    teacher_engine.add_axiom(l)
    teacher_engine.add_axiom(r)
    
    axiom = RightTerminology(ConceptExpression("A"), expr("B", "C"))
    
    teacher_engine.add_axiom(axiom)
    
    counter_example = axiom
    
    axiom = learner.saturate_right(counter_example)
    
    assert axiom == RightTerminology(ConceptExpression("A"), expr("B","C","D","E","F"))
    
"""    

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
    """