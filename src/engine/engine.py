from typing import Protocol, List
from src.data.special import RightTerminology, LeftTerminology
from src.data.communication import InclusionAxiom, ConceptExpression

class Engine(Protocol):
    """The engine is what the Learner uses to do operations on its hypothesis ontology.
    """
    def entails(self, axiom: RightTerminology | LeftTerminology | InclusionAxiom) -> bool:
        """The method should implement whether or not an axiom is entailed by the engines ontology

        Args:
            axiom (RightTerminology | LeftTerminology | InclusionAxiom): The axiom to test

        Returns:
            bool: True if the axiom is entailed from the engines ontology
        """
        ...
    
    def add_axiom(self, axiom: RightTerminology | LeftTerminology):
        """Adds an axiom to the engines ontology. If there is a terminology with that given concept, it gets overwritten.

        Args:
            axiom (RightTerminology | LeftTerminology): Axiom to be added
        """
        ...
    
    def get_hypothesis(self) -> List[RightTerminology | LeftTerminology]:
        """Get the ontology in form of axioms

        Returns:
            List[Right | Left]: The ontology as a list of axioms
        """
        ...
    
    def get_right_from_hypothesis(self, concept_expression: ConceptExpression) -> RightTerminology | None:
        """Gets a right terminology based on a given concept expression.

        Args:
            concept_expression (ConceptExpression): The concept expression that is used when getting the terminology

        Returns:
            RightTerminology | None: Returns the given right terminology. Returns None if it does not exist.
        """
        ...