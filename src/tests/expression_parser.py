
from typing import Dict, List

from src.data.communication import Concept, Role, Expression

ExprItems = str | Dict[str, List['ExprItems']]

def expr(*args: ExprItems) -> Expression:
    return expr_list(list(args))

def expr_list(args: List[ExprItems]) -> Expression:
    concepts: List[Concept] = list()
    roles: List[Role] = list()
    
    for a in args:
        if isinstance(a, str):
            concepts.append(Concept(a))
        else:
            for k, v in a.items():
                e = expr_list(v)
                roles.append(Role(k, e))
    
    e = Expression(concepts, roles)
    return e