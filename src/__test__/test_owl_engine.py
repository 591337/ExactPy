import pytest
import owlready2

from src.dataclass import Right, Left
from src.engine import OwlEngine

from src.protocols import *

def test_add_simple_left_axiom():
    """Testing adding a simple left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.⊤ ⊑ Animal
    left_axiom = Left(Expression([Role("eats", Expression([]))]), Consept("Animal"))
    engine.addAxiom(left_axiom)
    
    left_axioms = list(onto.general_class_axioms())
    
    assert len(left_axioms) is 1
    assert len(left_axioms[0].is_a) is 1
            
    onto.destroy()

def test_add_list_left_axiom():
    """Testing adding a complex left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.(∃.eats.⊤ ⊓ Mouse) ⊑ Animal
    left_axiom = Left(Expression([Role("eats", Expression([Role("eats", Expression([]))])), Consept("Mouse")]), Consept("Animal"))
    engine.addAxiom(left_axiom)
    
    left_axioms = list(onto.general_class_axioms())
    
    assert len(left_axioms) is 1
    assert len(left_axioms[0].is_a) is 1
        
    onto.destroy()

def test_add_right_axiom():
    """Testing adding a complex right axiom (EL_rhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Animal ⊑ ∃.eats.(∃.eats.⊤ ⊓ Mouse)
    right_axiom = Right(Consept("Animal"), Expression([Role("eats", Expression([Role("eats", Expression([]))])), Consept("Mouse")]))
    
    engine.addAxiom(right_axiom)
    animal = onto.Animal
    
    assert animal is not None
    assert len(animal.is_a) is 2 # the thing above + owl.Thing
    
    onto.destroy()
    
def test_entails_right():  
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Mother ⊑ ∃.parent_of.Mother
    right_axiom = Right(Consept("Mother"), Expression([Role("parentOf", Expression([Consept("Mother")]))]))
    engine.addAxiom(right_axiom)
    
    # entails: Mother ⊑ ∃.parent_of.⊤
    assert engine.entails(Right(Consept("Mother"), Expression([Role("parentOf", Expression([]))])))
    # does not entail: Mother ⊑ ∃.parent_of.⊤
    assert not engine.entails(Right(Consept("Mother"), Expression([Role("parentOf", Expression([Consept("Father")]))])))
    # entails: Mother ⊑ ∃.parent_of.(∃.parent_of.⊤)
    assert engine.entails(Right(Consept("Mother"), Expression([Role("parentOf", Expression([Role("parentOf", Expression([]))]))])))
    
    onto.destroy()
    
def test_entails_left():
    """Testing if entails works for Left axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # ∃.parent_of.Parent ⊑ Parent
    # Mother ⊑ Parent
    left_axiom = Left(Expression([Role("parentOf", Expression([Consept("Parent")]))]), Consept("Parent"))
    right_axiom = Right(Consept("Mother"), Expression([Consept("Parent")]))
    engine.addAxiom(left_axiom)
    engine.addAxiom(right_axiom)
    
    # entails: ∃.parent_of.Mother ⊑ Parent
    assert engine.entails(Left(Expression([Role("parentOf", Expression([Consept("Mother")]))]), Consept("Parent")))
    # does not etail: ∃.parent_of.⊤ ⊑ Parent
    assert not engine.entails(Left(Expression([Role("parentOf", Expression([]))]), Consept("Parent")))
    
    onto.destroy()
