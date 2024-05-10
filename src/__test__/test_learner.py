import pytest
import owlready2

from src.__test__.expression_parser import expr
from src.dataclass import Right, Left
from src.engine import OwlEngine

from src.__test__.teacher_mock import TestTeacher

from src.learner import LearnerImpl

from src.protocols import Consept

def test_is_counter_example():
    """Checking the counter example test 
    """
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("Mother"), Consept("Parent"), Consept("Person")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    # ∃.eats.⊤ ⊑ Person
    
    axiom = Left(expr({"eats":[]}), Consept("Mother"))
    teacher_engine.add_axiom(axiom)
    
    # ∃.eats.⊤ ⊑ Mother
    assert learner._is_counter_example(Left(expr({"eats": []}), Consept("Mother")))
    # ∃.eats.Peron ⊑ Mother
    assert learner._is_counter_example(Left(expr({"eats": ["Person"]}), Consept("Mother")))
    # not ∃.eats.Peron ⊑ Person
    assert not learner._is_counter_example(Left(expr({"eats": ["Person"]}), Consept("Person")))
    
    # Mother ⊑ Person
    axiom = Right(Consept("Mother"), expr("Person"))
    teacher_engine.add_axiom(axiom)

    # Mother ⊑ Person
    assert learner._is_counter_example(Left(expr("Mother"), Consept("Person")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Left(expr({"eats": ["Person"]}), Consept("Person")))
    
    # ∃.eats.⊤ ⊑ Person
    axiom = Left(expr({"eats":[]}), Consept("Mother"))
    engine.add_axiom(axiom)
    
    # not ∃.eats.⊤ ⊑ Mother
    assert not learner._is_counter_example(Left(expr({"eats":[]}), Consept("Mother")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Left(expr({"eats":["Person"]}), Consept("Person")))
    
    onto.destroy()

def test_right_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("Human"), Consept("Dog")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Right(Consept("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Right(Consept("Human"), expr({"hasParent": ["Human", {"hasParent": []}]}))
    
    axiom = learner.saturate_right(counter_example)
        
    assert isinstance(axiom, Right)
    
    assert len(axiom.right.consepts) == 0
    
    assert len(axiom.right.roles) == 1
    
    expression = axiom.right.roles[0].expression
    
    assert len(expression.consepts) == 1
    
    assert expression.consepts[0].name == "Human"
    
    assert len(expression.roles) == 1
    
    expression = expression.roles[0].expression
    
    assert len(expression.consepts) == 1
    
    assert expression.consepts[0].name == "Human"
    
    assert len(expression.roles) == 0

def test_right_decompesision():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("Woman"), Consept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Right(Consept("Woman"), expr("Human"))
    teacher_engine.add_axiom(axiom)
    axiom = Right(Consept("Human"), expr({"hasParent": ["Human"]}))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Right(Consept("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
        
    assert isinstance(axiom, Right)
    
    assert axiom.left.name == "Human"
    
    assert len(axiom.right.consepts) == 0
    
    assert len(axiom.right.roles) == 1
    
    assert axiom.right.roles[0].name == "hasParent"
    
    expression = axiom.right.roles[0].expression
    
    assert len(expression.consepts) == 1
    
    assert expression.consepts[0].name == "Human"
    
    assert len(expression.roles) == 0
    
    engine.add_axiom(axiom)
    
    counter_example = Right(Consept("Woman"), expr("Human", {"hasParent": ["Human", {"hasParent": ["Human"]}]}))
    axiom = learner.decompose_right(counter_example)
    
    assert isinstance(axiom, Right)
    
    assert axiom.left.name == "Woman"
    
    assert len(axiom.right.consepts) == 1
    
    assert axiom.right.consepts[0].name == "Human"
    
    assert len(axiom.right.roles) == 0

def test_left_saturation():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("Cat"), Consept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Left(expr({"hasParent": []}), Consept("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = Left(expr({"hasChild": ["Human"]}), Consept("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Left(expr({"hasChild": [{"hasParent": []}]}), Consept("Human"))
    
    axiom = learner.saturate_left(counter_example)
    
    assert len(axiom.left.consepts) == 0
    
    assert len(axiom.left.roles) == 1
    
    expression = axiom.left.roles[0].expression
    
    assert len(expression.consepts) == 1
    
    assert expression.consepts[0].name == "Human"

def test_left_decomposision():
    onto = owlready2.get_ontology("http://test-teacher.org/onto.owl")
    teacher_engine = OwlEngine(onto)
    teacher = TestTeacher(teacher_engine, [Consept("Cat"), Consept("Human")])
    
    onto = owlready2.get_ontology("http://test-learner.org/onto.owl")
    engine = OwlEngine(onto)
    learner = LearnerImpl(engine, teacher)
    
    axiom = Left(expr({"hasParent": []}), Consept("Human"))
    teacher_engine.add_axiom(axiom)
    engine.add_axiom(axiom)
    
    axiom = Left(expr({"hasChild": ["Human"]}), Consept("Human"))
    teacher_engine.add_axiom(axiom)
    
    counter_example = Left(expr({"hasChild": [{"hasParent": []}, "Human"]}), Consept("Human"))
    
    axiom = learner.decompose_left(counter_example)
    
    assert len(axiom.left.consepts) == 0
    
    assert len(axiom.left.roles) == 1
    
    expression = axiom.left.roles[0].expression
    
    assert len(expression.consepts) == 1
    
    assert expression.consepts[0].name == "Human"
    