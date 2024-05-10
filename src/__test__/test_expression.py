import pytest

from src.__test__.expression_parser import expr
from src.protocols import Expression

def test_iteratior():
    exp = expr("1", {"2": ["2"]}, {"3": ["3"]})
    
    it = iter(exp)
    
    e = next(it)
    
    assert e is exp
    
    assert isinstance(e, Expression)
    assert e.consepts[0].name == "1"
        
    assert e.roles.pop(0).name == "2"
    
    e = next(it)
    
    assert e is exp.roles[0].expression
    
    assert e.consepts[0].name == "3"