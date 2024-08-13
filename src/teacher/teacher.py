
from typing import List, Protocol
from src.data.communication import InclusionAxiom, ConceptExpression

class Teacher(Protocol):
    """The teacher is who the learner asks questions to in order to learn the ontology
    """
    def membership_query(self, axiom: InclusionAxiom) -> bool:
        """Checks if an axiom is the member of the target ontology

        Args:
            axiom (InclusionAxiom): the axiom to check against the ontology

        Returns:
            bool: true if the axiom is a logical consequence of the ontology
        """
        ...
    
    def equivalence_query(self, axioms: List[InclusionAxiom]) -> InclusionAxiom | None:
        """Checks if an hypothesis ontology is equivalent with the target ontology. It gives
        an counter example if it is not true.

        Args:
            axioms (List[InclusionAxiom]): The hypothesis ontology to be check against the target. 

        Returns:
            InclusionAxiom | None: If it is not a logical consequence, it returns an counter example.
            if it is a logical consequence, it returns None.
        """
        ...
    
    def get_concepts(self) -> List[ConceptExpression]:
        """The learner is responsible to know what concepts expression and roles the ontology consists of.

        Returns:
            List[ConceptExpression]: The concepts of the ontology.
        """
        ...
        

