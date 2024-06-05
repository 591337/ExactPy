import pytest

from src.tests.expression_parser import expr
from src.data.communication import Node, Role, ConceptExpression

def test_iterator():
    exp = expr("1", {"2": ["2"]}, {"3": ["3"]})
    
    it = iter(exp)
    
    e = next(it)
    
    assert e is exp
    
    assert isinstance(e, Node)
    assert e.labels[0] == ConceptExpression("1")
        
    assert e.edges.pop(0).label == Role("2")
    
    e = next(it)
    
    assert e is exp.edges[0].target
    
    assert e.labels[0] == ConceptExpression("3")