import pytest
import owlready2

from src.tests.expression_parser import expr
from src.data.special import RightTerminology, LeftTerminology
from src.engine.engine_impl import OwlEngine

from src.tests.teacher_mock import TestTeacher

from src.learner.learner_impl import LearnerImpl

from src.data.communication import ConceptExpression

def test_is_counter_example():
    """Checking the counter example test 
    """
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Mother"), ConceptExpression("Parent"), ConceptExpression("Person")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    # ∃.eats.⊤ ⊑ Person
    
    axiom = LeftTerminology(expr({"eats":[]}), ConceptExpression("Mother"))
    teacher_engine.add_axiom(axiom)
    
    # ∃.eats.⊤ ⊑ Mother
    assert learner._is_counter_example(LeftTerminology(expr({"eats": []}), ConceptExpression("Mother")))
    # ∃.eats.Peron ⊑ Mother
    assert learner._is_counter_example(LeftTerminology(expr({"eats": ["Person"]}), ConceptExpression("Mother")))
    # not ∃.eats.Peron ⊑ Person
    assert not learner._is_counter_example(LeftTerminology(expr({"eats": ["Person"]}), ConceptExpression("Person")))
    
    # Mother ⊑ Person
    axiom = RightTerminology(ConceptExpression("Mother"), expr("Person"))
    teacher_engine.add_axiom(axiom)

    # Mother ⊑ Person
    assert learner._is_counter_example(LeftTerminology(expr("Mother"), ConceptExpression("Person")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(LeftTerminology(expr({"eats": ["Person"]}), ConceptExpression("Person")))
    
    # ∃.eats.⊤ ⊑ Person
    axiom = LeftTerminology(expr({"eats":[]}), ConceptExpression("Mother"))
    engine.add_axiom(axiom)
    
    # not ∃.eats.⊤ ⊑ Mother
    assert not learner._is_counter_example(LeftTerminology(expr({"eats":[]}), ConceptExpression("Mother")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(LeftTerminology(expr({"eats":["Person"]}), ConceptExpression("Person")))
    
    onto.destroy()

def test_right_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Human"), ConceptExpression("Dog")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human", {"hasParent": []}]}))
    
    axiom = learner.saturate_right(counter_example)
    
    assert axiom == RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human", {"hasParent": ["Human"]}]}))

def test_right_decomposition():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Woman"), ConceptExpression("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = RightTerminology(ConceptExpression("Woman"), expr("Human"))
    teacher_engine.add_axiom(axiom)
    axiom = RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = RightTerminology(ConceptExpression("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
    
    assert axiom == RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human"]}))
    
    engine.add_axiom(axiom)
    
    counter_example = RightTerminology(ConceptExpression("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
    
    assert axiom == RightTerminology(ConceptExpression("Woman"), expr("Human"))

def test_left_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Cat"), ConceptExpression("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = LeftTerminology(expr({"hasParent": []}), ConceptExpression("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = LeftTerminology(expr({"hasChild": ["Human"]}), ConceptExpression("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = LeftTerminology(expr({"hasChild": [{"hasParent": []}]}), ConceptExpression("Human"))
    
    axiom = learner.saturate_left(counter_example)
    
    assert axiom == LeftTerminology(expr({"hasChild": [{"hasParent": []}, "Human"]}), ConceptExpression("Human"))

def test_left_decomposition():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Cat"), ConceptExpression("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = LeftTerminology(expr({"hasParent": []}), ConceptExpression("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = LeftTerminology(expr({"hasChild": ["Human"]}), ConceptExpression("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = LeftTerminology(expr({"hasChild": [{"hasParent": []}, "Human"]}), ConceptExpression("Human"))
    
    axiom = learner.decompose_left(counter_example)
        
    assert axiom == LeftTerminology(expr({"hasChild": ["Human"]}), ConceptExpression("Human"))

def test_sibling_merge():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [ConceptExpression("Male"), ConceptExpression("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    target_axiom = RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human", "Male"]}))
    teacher_engine.add_axiom(target_axiom)
    
    counter_example = RightTerminology(ConceptExpression("Human"), expr({"hasParent": ["Human"]}, {"hasParent": ["Male"]}))
    
    axiom = learner.sibling_merge(counter_example)
    
    assert target_axiom == axiom