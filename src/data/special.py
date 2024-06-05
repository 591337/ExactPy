from __future__ import annotations
from typing import List

from dataclasses import dataclass

from src.data.communication import ConceptExpression, Node, InclusionAxiom

@dataclass
class RightTerminology:
    """A inclusion consisting of a left ConceptExpression and right complex expression (node). This is know as a EL_rhs
    
    Mother ⊑ ∃.parent_of.⊤
    """
    left: ConceptExpression
    right: Node
    
    def inclusion_axiom(self) -> InclusionAxiom:
        """Converts the left inclusion into a general inclusion

        Returns:
            InclusionAxiom: Axiom as an inclusion
        """
        return InclusionAxiom(Node([self.left], []), self.right)

@dataclass
class LeftTerminology:
    """A inclusion consisting of a left complex expression (node) and right ConceptExpression. This is know as a EL_lhs
    
    ∃.parent_of.⊤ ⊑ Mother
    """
    left: Node
    right: ConceptExpression
    
    def inclusion_axiom(self) -> InclusionAxiom:
        """Converts the left inclusion into a general inclusion

        Returns:
            InclusionAxiom: Axiom as an inclusion
        """
        return InclusionAxiom(self.left, Node([self.right], []))
