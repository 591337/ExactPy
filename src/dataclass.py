from __future__ import annotations
from typing import List

from dataclasses import dataclass

from src.protocols import Consept, Expression, InclutionAxiom

@dataclass
class Left:
    """A incluton consisting of a left Consept and right Expression. This is know as a EL_lhs
    
    Consept ⊑ Expression
    """
    left: Consept
    right: Expression
    
    def inclution_axiom(self) -> InclutionAxiom:
        """Converts the left inclution into a general inclution

        Returns:
            InclutionAxiom: Axiom as an inclution
        """
        return InclutionAxiom(Expression([self.left]), self.right)

@dataclass
class Right:
    """A incluton consisting of a left Expression and right Consept. This is know as a EL_rhs
    
    Expression ⊑ Consept
    """
    left: Expression
    right: Consept
    
    def inclution_axiom(self) -> InclutionAxiom:
        """Converts the left inclution into a general inclution

        Returns:
            InclutionAxiom: Axiom as an inclution
        """
        return InclutionAxiom(self.left, Expression([self.right]))
