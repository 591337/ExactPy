from typing import Protocol, List
from src.data.special import Right, Left
from src.data.communication import InclutionAxiom, Concept

class Engine(Protocol):
    """The engine is what the Learner uses to do operations on its hypothosis ontology.
    """
    def entails(self, axiom: Right | Left | InclutionAxiom) -> bool:
        """The method should implement wreather ot not an axiom is entailed by the engines ontology

        Args:
            axiom (Right | Left | InclutionAxiom): The axiom to test

        Returns:
            bool: True if the axiom is entailed from the engines ontology
        """
        ...
    
    def add_axiom(self, axiom: Right | Left): # TODO: Should this one override existing once? Could they be merged in case they are doubled
        """Adds an axiom to the engines ontology

        Args:
            axiom (Right | Left): Axiom to be added
        """
        ...
    
    def get_hypothisis(self) -> List[Right | Left]:
        """Get the onology in form of axioms

        Returns:
            List[Right | Left]: The ontology as a list of axioms
        """
        ...
    
    def get_right_from_hypothisis(self, concept: Concept) -> Right | None:
        """Gets the 

        Args:
            concept (Consept): _description_

        Returns:
            Right | None: _description_
        """
        ...