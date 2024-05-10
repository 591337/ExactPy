import pytest

from src.__test__.expression_parser import expr
from src.protocols import Expression

def test_iteratior():
    e = expr("1", {"2": ["2"]}, {"3": ["3"]})
    
    exp = iter(e)
    
    assert exp is e
    
    assert isinstance(exp, Expression)
    assert exp.consepts[0].name == "1"
        
    assert exp.roles.pop(0).name == "2"
    
    exp = next(exp)
    
    assert exp is e.roles[0].expression
    
    assert exp.consepts[0].name == "3"