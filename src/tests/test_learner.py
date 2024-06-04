import pytest
import owlready2

from src.tests.expression_parser import expr
from src.data.special import Right, Left
from src.engine.engine_impl import OwlEngine

from src.tests.teacher_mock import TestTeacher

from src.learner.learner_impl import LearnerImpl

from src.data.communication import Concept

def test_is_counter_example():
    """Checking the counter example test 
    """
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Mother"), Concept("Parent"), Concept("Person")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    # ∃.eats.⊤ ⊑ Person
    
    axiom = Left(expr({"eats":[]}), Concept("Mother"))
    teacher_engine.add_axiom(axiom)
    
    # ∃.eats.⊤ ⊑ Mother
    assert learner._is_counter_example(Left(expr({"eats": []}), Concept("Mother")))
    # ∃.eats.Peron ⊑ Mother
    assert learner._is_counter_example(Left(expr({"eats": ["Person"]}), Concept("Mother")))
    # not ∃.eats.Peron ⊑ Person
    assert not learner._is_counter_example(Left(expr({"eats": ["Person"]}), Concept("Person")))
    
    # Mother ⊑ Person
    axiom = Right(Concept("Mother"), expr("Person"))
    teacher_engine.add_axiom(axiom)

    # Mother ⊑ Person
    assert learner._is_counter_example(Left(expr("Mother"), Concept("Person")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Left(expr({"eats": ["Person"]}), Concept("Person")))
    
    # ∃.eats.⊤ ⊑ Person
    axiom = Left(expr({"eats":[]}), Concept("Mother"))
    engine.add_axiom(axiom)
    
    # not ∃.eats.⊤ ⊑ Mother
    assert not learner._is_counter_example(Left(expr({"eats":[]}), Concept("Mother")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Left(expr({"eats":["Person"]}), Concept("Person")))
    
    onto.destroy()

def test_right_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Human"), Concept("Dog")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Right(Concept("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Right(Concept("Human"), expr({"hasParent": ["Human", {"hasParent": []}]}))
    
    axiom = learner.saturate_right(counter_example)
    
    assert axiom == Right(Concept("Human"), expr({"hasParent": ["Human", {"hasParent": ["Human"]}]}))

def test_right_decompesision():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Woman"), Concept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Right(Concept("Woman"), expr("Human"))
    teacher_engine.add_axiom(axiom)
    axiom = Right(Concept("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Right(Concept("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
    
    assert axiom == Right(Concept("Human"), expr({"hasParent": ["Human"]}))
    
    engine.add_axiom(axiom)
    
    counter_example = Right(Concept("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
    
    assert axiom == Right(Concept("Woman"), expr("Human"))

def test_left_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Cat"), Concept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Left(expr({"hasParent": []}), Concept("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = Left(expr({"hasChild": ["Human"]}), Concept("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Left(expr({"hasChild": [{"hasParent": []}]}), Concept("Human"))
    
    axiom = learner.saturate_left(counter_example)
    
    assert axiom == Left(expr({"hasChild": [{"hasParent": []}, "Human"]}), Concept("Human"))

def test_left_decomposision():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Cat"), Concept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Left(expr({"hasParent": []}), Concept("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = Left(expr({"hasChild": ["Human"]}), Concept("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Left(expr({"hasChild": [{"hasParent": []}, "Human"]}), Concept("Human"))
    
    axiom = learner.decompose_left(counter_example)
        
    assert axiom == Left(expr({"hasChild": ["Human"]}), Concept("Human"))

def test_sibling_merge():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Concept("Male"), Concept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    target_axiom = Right(Concept("Human"), expr({"hasParent": ["Human", "Male"]}))
    teacher_engine.add_axiom(target_axiom)
    
    counter_example = Right(Concept("Human"), expr({"hasParent": ["Human"]}, {"hasParent": ["Male"]}))
    
    axiom = learner.sibling_merge(counter_example)
    
    assert target_axiom == axiom