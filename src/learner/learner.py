from typing import Protocol, List
from src.data.communication import InclutionAxiom

class Learner(Protocol):
    """The learner is the basis of the Angluin's exact learning framework.
    It inteacts with a teacher by sending it queries.
    """
    def run_learner(self) -> List[InclutionAxiom]:
        ...