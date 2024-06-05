
from typing import Dict, List

from src.data.communication import ConceptExpression, Edge, Node, Role

ExprItems = str | Dict[str, List['ExprItems']]

def expr(*args: ExprItems) -> Node:
    return expr_list(list(args))

def expr_list(args: List[ExprItems]) -> Node:
    concepts: List[ConceptExpression] = list()
    roles: List[Edge] = list()
    
    for a in args:
        if isinstance(a, str):
            concepts.append(ConceptExpression(a))
        else:
            for k, v in a.items():
                e = expr_list(v)
                roles.append(Edge(Role(k), e))
    
    e = Node(concepts, roles)
    return e