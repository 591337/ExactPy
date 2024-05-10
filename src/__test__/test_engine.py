import pytest
import owlready2

from src.__test__.expression_parser import expr
from src.dataclass import Right, Left
from src.engine import OwlEngine

from src.protocols import Consept

def test_add_right_axiom_with_left_consept():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Mother ⊑ Parent
    axiom = Left(expr("Mother"), Consept("Parent"))
    engine.add_axiom(axiom)
    
    left_axioms = list(onto.general_class_axioms())
    left_axioms.extend(onto.classes())
    
    assert len(left_axioms) == 2

def test_add_simple_right_axiom():
    """Testing adding a simple left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.⊤ ⊑ Animal
    left_axiom = Left(expr({"eats": []}), Consept("Animal"))
    engine.add_axiom(left_axiom)
    
    right_axioms = list(onto.general_class_axioms())
    
    assert len(right_axioms) == 1
    assert len(right_axioms[0].is_a) == 1
            
    onto.destroy()

def test_add_list_right_axiom():
    """Testing adding a complex left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # ∃.eats.(∃.eats.⊤ ⊓ Mouse) ⊑ Animal
    axiom = Left(expr({"eats": [{"eats": []}, "Mouse"]}), Consept("Animal"))
    engine.add_axiom(axiom)
    
    axioms = list(onto.general_class_axioms())
    
    assert len(axioms) == 1
    assert len(axioms[0].is_a) == 1
        
    onto.destroy()

def test_add_left_axiom():
    """Testing adding a complex left axiom (EL_lhs) to an empty ontology
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Animal ⊑ ∃.eats.(∃.eats.⊤ ⊓ Mouse)
    axiom = Right(Consept("Animal"), expr({"eats": [{"eats": []}, "Mouse"]}))
    
    engine.add_axiom(axiom)
    animal = onto.Animal
    
    assert animal is not None
    assert len(animal.is_a) == 2 # the thing above + owl.Thing
    
    onto.destroy()
    
def test_entails_left():  
    """Testing if entails works for Left axioms (EL_lhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    engine = OwlEngine(onto)
    
    # Mother ⊑ ∃.parent_of.Mother
    axiom = Right(Consept("Mother"), expr({"parent_of": ["Mother"]}))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ ∃.parent_of.⊤
    assert engine.entails(Right(Consept("Mother"), expr({"parent_of": []})))
    # does not entail: Mother ⊑ ∃.parent_of.Father
    assert not engine.entails(Right(Consept("Mother"), expr({"parent_of": ["Father"]})))
    # entails: Mother ⊑ ∃.parent_of.(∃.parent_of.⊤)
    assert engine.entails(Right(Consept("Mother"), expr({"parent_of": [{"parent_of": []}]})))
    
    onto.destroy()
    
def test_entails_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # ∃.parent_of.Parent ⊑ Parent
    # Mother ⊑ Parent
    axiom_1 = Left(expr({"parent_of": ["Parent"]}), Consept("Parent"))
    axiom_2 = Right(Consept("Mother"), expr("Parent"))
    engine.add_axiom(axiom_1)
    engine.add_axiom(axiom_2)
    
    # entails: ∃.parent_of.Mother ⊑ Parent
    assert engine.entails(Left(expr({"parent_of": ["Mother"]}), Consept("Parent")))
    # does not etail: ∃.parent_of.⊤ ⊑ Parent
    assert not engine.entails(Left(expr({"parent_of": []}), Consept("Parent")))
    
    onto.destroy()

def test_entails_right_left():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = Left(expr("Mother"), Consept("Parent"))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(Right(Consept("Mother"), expr("Parent")))
                          
    onto.destroy()

def test_entails_left_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = Right(Consept("Mother"), expr("Parent"))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(Left(expr("Mother"), Consept("Parent")))
                          
    onto.destroy()
