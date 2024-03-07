import pytest
import owlready2
from src.dataclass import *
from src.engine import OwlEngine

def test_add_simple_left_axiom():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    left_axiom = Left(Node([Relation("eats", Node([]))]), Class("Animal"))
    
    engine.addAxiom(left_axiom)
    
    left_axioms = list(onto.general_class_axioms())
    
    assert len(left_axioms) is 1
    assert len(left_axioms[0].is_a) is 1
            
    onto.destroy()

def test_add_list_left_axiom():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    left_axiom = Left(Node([Relation("eats", Node([Relation("eats", Node([]))])), Class("Mouse")]), Class("Animal"))
    
    engine.addAxiom(left_axiom)
    
    left_axioms = list(onto.general_class_axioms())
    
    assert len(left_axioms) is 1
    assert len(left_axioms[0].is_a) is 1
        
    onto.destroy()

def test_add_right_axiom():
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    right_axiom = Right(Class("Animal"), Node([Relation("eats", Node([Relation("eats", Node([]))])), Class("Mouse")]))
    
    engine.addAxiom(right_axiom)
    
    animal = onto.Animal
    
    assert animal is not None
    assert len(animal.is_a) is 2 # the thing above + owl.Thing
    
    onto.destroy()
    
def test_entails_right():    
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    right_axiom = Right(Class("Mother"), Node([Relation("parentOf", Node([Class("Mother")]))]))
    
    engine.addAxiom(right_axiom)
    
    assert engine.entails(Right(Class("Mother"), Node([Relation("parentOf", Node([]))])))
    
    assert not engine.entails(Right(Class("Mother"), Node([Relation("parentOf", Node([Class("Father")]))])))
    
    assert engine.entails(Right(Class("Mother"), Node([Relation("parentOf", Node([Relation("parentOf", Node([]))]))])))
    
    onto.destroy()
    
def test_entails_left():    
    onto = owlready2.get_ontology("http://test.org/onto.owl")
    
    engine = OwlEngine(onto)
    
    left_axiom = Left(Node([Relation("parentOf", Node([Class("Parent")]))]), Class("Parent"))
    
    engine.addAxiom(left_axiom)
    
    right_axiom = Right(Class("Mother"), Node([Class("Parent")]))
    
    engine.addAxiom(right_axiom)
    
    assert engine.entails(Left(Node([Relation("parentOf", Node([Class("Mother")]))]), Class("Parent")))
    
    assert not engine.entails(Left(Node([Relation("parentOf", Node([]))]), Class("Parent")))
    
    onto.destroy()
