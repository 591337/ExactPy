
from typing import List, Protocol
from src.data.communication import InclutionAxiom, Concept

class Teacher(Protocol):
    """The teacher is who the learner askes questions to in order to learn the ontology
    """
    def membership_query(self, axiom: InclutionAxiom) -> bool:
        """Checks if an axiom is the member of the target ontology

        Args:
            axiom (InclutionAxiom): the axiom to check against the ontology

        Returns:
            bool: true if the axiom is a logical consequense of the ontology
        """
        ...
    
    def equivalence_query(self, axioms: List[InclutionAxiom]) -> InclutionAxiom | None:
        """Checks if an hypothesis ontology is equivalent with the target ontology. It gives
        an counter example if it is not true.

        Args:
            axioms (List[InclutionAxiom]): The hypothesis ontology to be check against the target. 

        Returns:
            InclutionAxiom | None: If it is not a logical consequense, it returns an counter example.
            if it is a logical consequense, it returns None.
        """
        ...
    
    def get_concepts(self) -> List[Concept]:
        """The learner is responsible to know what Consepts and Roles the ontology consists of.

        Returns:
            List[Consept]: The concepts of the ontology.
        """
        ...