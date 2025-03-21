import pytest
import owlready2

from src.tests.expression_parser import expr
from src.data.special import RightTerminology, LeftTerminology
from src.engine.engine_impl import OwlEngine

from src.data.communication import ConceptExpression

def test_add_right_axiom_with_left_concept():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Mother ⊑ Parent
    axiom = LeftTerminology(expr("Mother"), ConceptExpression("Parent"))
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
    left_axiom = LeftTerminology(expr({"eats": []}), ConceptExpression("Animal"))
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
    axiom = LeftTerminology(expr({"eats": [{"eats": []}, "Mouse"]}), ConceptExpression("Animal"))
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
    axiom = RightTerminology(ConceptExpression("Animal"), expr({"eats": [{"eats": []}, "Mouse"]}))
    
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
    axiom = RightTerminology(ConceptExpression("Mother"), expr({"parent_of": ["Mother"]}))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ ∃.parent_of.⊤
    assert engine.entails(RightTerminology(ConceptExpression("Mother"), expr({"parent_of": []})))
    # does not entail: Mother ⊑ ∃.parent_of.Father
    assert not engine.entails(RightTerminology(ConceptExpression("Mother"), expr({"parent_of": ["Father"]})))
    # entails: Mother ⊑ ∃.parent_of.(∃.parent_of.⊤)
    assert engine.entails(RightTerminology(ConceptExpression("Mother"), expr({"parent_of": [{"parent_of": []}]})))
    
    onto.destroy()
    
def test_entails_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # ∃.parent_of.Parent ⊑ Parent
    # Mother ⊑ Parent
    axiom_1 = LeftTerminology(expr({"parent_of": ["Parent"]}), ConceptExpression("Parent"))
    axiom_2 = RightTerminology(ConceptExpression("Mother"), expr("Parent"))
    engine.add_axiom(axiom_1)
    engine.add_axiom(axiom_2)
    
    # entails: ∃.parent_of.Mother ⊑ Parent
    assert engine.entails(LeftTerminology(expr({"parent_of": ["Mother"]}), ConceptExpression("Parent")))
    # does not etail: ∃.parent_of.⊤ ⊑ Parent
    assert not engine.entails(LeftTerminology(expr({"parent_of": []}), ConceptExpression("Parent")))
    
    onto.destroy()

def test_entails_right_left():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = LeftTerminology(expr("Mother"), ConceptExpression("Parent"))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(RightTerminology(ConceptExpression("Mother"), expr("Parent")))
                          
    onto.destroy()

def test_entails_left_right():
    """Testing if entails works for Right axioms (EL_rhs)
    """
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    # Ontology
    # Mother ⊑ Parent
    axiom = RightTerminology(ConceptExpression("Mother"), expr("Parent"))
    engine.add_axiom(axiom)
    
    # entails: Mother ⊑ Parent
    assert engine.entails(LeftTerminology(expr("Mother"), ConceptExpression("Parent")))
                          
    onto.destroy()
