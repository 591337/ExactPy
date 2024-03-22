import pytest
import owlready2

from src.dataclass import Left, Right
from src.engine import OwlEngine

from src.__test__.teacher_mock import TestTeacher

from src.learner import LearnerImpl

from src.protocols import *

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
    axiom = Right(Expression([Role("eats", Expression([]))]), Consept("Mother"))
    teacher_engine.add_axiom(axiom)
    
    # ∃.eats.⊤ ⊑ Mother
    assert learner._is_counter_example(Right(Expression([Role("eats", Expression([]))]), Consept("Mother")))
    # ∃.eats.Peron ⊑ Mother
    assert learner._is_counter_example(Right(Expression([Role("eats", Expression([Consept("Person")]))]), Consept("Mother")))
    # not ∃.eats.Peron ⊑ Person
    assert not learner._is_counter_example(Right(Expression([Role("eats", Expression([]))]), Consept("Person")))
    
    # Mother ⊑ Person
    axiom = Left(Consept("Mother"), Expression([Consept("Person")]))
    teacher_engine.add_axiom(axiom)

    # Mother ⊑ Person
    assert learner._is_counter_example(Right(Expression([Consept("Mother")]), Consept("Person")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Right(Expression([Role("eats", Expression([]))]), Consept("Person")))
    
    # ∃.eats.⊤ ⊑ Person
    axiom = Right(Expression([Role("eats", Expression([]))]), Consept("Mother"))
    engine.add_axiom(axiom)
    
    # not ∃.eats.⊤ ⊑ Mother
    assert not learner._is_counter_example(Right(Expression([Role("eats", Expression([]))]), Consept("Mother")))
    # ∃.eats.Peron ⊑ Person
    assert learner._is_counter_example(Right(Expression([Role("eats", Expression([]))]), Consept("Person")))
    
    onto.destroy()