import pytest
import owlready2

from src.dataclass import Left, Right
from src.engine import OwlEngine

from src.protocols import *

def test_add_right_axiom_with_left_consept():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Mother ⊑ Parent
    axiom = Right(Expression([Consept("Mother")]), Consept("Parent"))
    engine.add_axiom(axiom)
    
    left_axioms = list(onto.general_class_axioms())
    left_axioms.extend(onto.classes())
    
    assert len(left_axioms) is 2

def test_add_simple_right_axiom():
    """Testing adding a simple left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.⊤ ⊑ Animal
    left_axiom = Right(Expression([Role("eats", Expression([]))]), Consept("Animal"))
    engine.add_axiom(left_axiom)
    
    right_axioms = list(onto.general_class_axioms())
    
    assert len(right_axioms) is 1
    assert len(right_axioms[0].is_a) is 1
            
    onto.destroy()

def test_add_list_right_axiom():
    """Testing adding a complex left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.(∃.eats.⊤ ⊓ Mouse) ⊑ Animal
    axiom = Right(Expression([Role("eats", Expression([Role("eats", Expression([]))])), Consept("Mouse")]), Consept("Animal"))
    engine.add_axiom(axiom)
    
    axioms = list(onto.general_class_axioms())
    
    assert len(axioms) is 1
    assert len(axioms[0].is_a) is 1
        
    onto.destroy()

def test_add_left_axiom():
    """Testing adding a complex left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Animal ⊑ ∃.eats.(∃.eats.⊤ ⊓ Mouse)
    axiom = Left(Consept("Animal"), Expression([Role("eats", Expression([Role("eats", Expression([]))])), Consept("Mouse")]))
    
    engine.add_axiom(axiom)
    animal = onto.Animal
    
    assert animal is not None
    assert len(animal.is_a) is 2 # the thing above + owl.Thing
    
    onto.destroy()
    
def test_entails_left():  
    """Testing if entails works for Left axioms (EL_lhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Mother ⊑ ∃.parent_of.Mother
    axiom = Left(Consept("Mother"), Expression([Role("parentOf", Expression([Consept("Mother")]))]))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ ∃.parent_of.⊤
    assert engine.entails(Left(Consept("Mother"), Expression([Role("parentOf", Expression([]))])))
    # does not entail: Mother ⊑ ∃.parent_of.⊤
    assert not engine.entails(Left(Consept("Mother"), Expression([Role("parentOf", Expression([Consept("Father")]))])))
    # entails: Mother ⊑ ∃.parent_of.(∃.parent_of.⊤)
    assert engine.entails(Left(Consept("Mother"), Expression([Role("parentOf", Expression([Role("parentOf", Expression([]))]))])))
    
    onto.destroy()
    
def test_entails_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # ∃.parent_of.Parent ⊑ Parent
    # Mother ⊑ Parent
    axiom_1 = Right(Expression([Role("parentOf", Expression([Consept("Parent")]))]), Consept("Parent"))
    axiom_2 = Left(Consept("Mother"), Expression([Consept("Parent")]))
    engine.add_axiom(axiom_1)
    engine.add_axiom(axiom_2)
    
    # entails: ∃.parent_of.Mother ⊑ Parent
    assert engine.entails(Right(Expression([Role("parentOf", Expression([Consept("Mother")]))]), Consept("Parent")))
    # does not etail: ∃.parent_of.⊤ ⊑ Parent
    assert not engine.entails(Right(Expression([Role("parentOf", Expression([]))]), Consept("Parent")))
    
    onto.destroy()

def test_entails_right_left():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = Right(Expression([Consept("Mother")]), Consept("Parent"))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(Left(Consept("Mother"), Expression([Consept("Parent")])))
                          
    onto.destroy()

def test_entails_left_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = Left(Consept("Mother"), Expression([Consept("Parent")]))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(Right(Expression([Consept("Mother")]), Consept("Parent")))
                          
    onto.destroy()
