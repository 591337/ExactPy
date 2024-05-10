
from typing import Dict, Any, Set, List

from src.protocols import Consept, Role, Expression

ExprItems = str | Dict[str, List['ExprItems']]

def expr(*args: ExprItems) -> Expression:
    return expr_list(list(args))

def expr_list(args: List[ExprItems]) -> Expression:
    consepts: List[Consept] = list()
    roles: List[Role] = list()
    
    for a in args:
        if isinstance(a, str):
            consepts.append(Consept(a))
        else:
            for k, v in a.items():
                e = expr_list(v)
                roles.append(Role(k, e))
    
    e = Expression(consepts, roles)
    return e