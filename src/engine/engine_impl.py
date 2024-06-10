from dataclasses import dataclass
from typing import Any, Dict, List
from owlready2 import Ontology, And, GeneralClassAxiom, ObjectProperty, Thing, sync_reasoner, ThingClass, ObjectPropertyClass
import owlready2
from src.data.special import RightTerminology, LeftTerminology
import types
import os

from src.data.communication import ConceptExpression, Edge, Node, InclusionAxiom

owl_java = "JAVA_EXE"
if owl_java in os.environ:
    owlready2.JAVA_EXE = os.environ[owl_java]

@dataclass
class OntologyMap:
    """
    Object used for having control over axioms in the ontology. Only accepts Terminologies.
    """
    left_map: Dict[ConceptExpression, LeftTerminology]
    right_map: Dict[ConceptExpression, RightTerminology]
    
    def add_axiom(self, axiom: LeftTerminology | RightTerminology) -> None:
        """Adds a axiom to the ontology

        Args:
            axiom (LeftTerminology | RightTerminology): Axiom to add
        """
        if isinstance(axiom, LeftTerminology):
            self.left_map[axiom.right] = axiom
        elif isinstance(axiom, RightTerminology):
            self.right_map[axiom.left] = axiom
    
    def get_list(self) -> List[LeftTerminology | RightTerminology]:
        """Returns the ontology as a list of left and right terminologies.

        Returns:
            List[LeftTerminology | RightTerminology]: list of all axioms in the ontology.
        """
        l: List[LeftTerminology | RightTerminology] = list(self.left_map.values())
        l.extend(self.right_map.values())
        return l

class OwlEngine:
    """
    Implementation of the Engine protocol
    """
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology_list: OntologyMap = OntologyMap({}, {})
    
    def entails(self, axiom: RightTerminology | LeftTerminology | InclusionAxiom) -> bool:
        """The method should implement whether or not an axiom is entailed by the engines ontology.
        
        This implementation works by adding temporary concept expressions to the ontology and then
        removing it after checking for ancestors.

        Args:
            axiom (RightTerminology | LeftTerminology | InclusionAxiom): The axiom to test

        Returns:
            bool: True if the axiom is entailed from the engines ontology
        """
        
        if isinstance(axiom, InclusionAxiom):
            # Creates two concept expressions in order to get around the fact that the engine is made
            # with terminologies in mind
            temp_sub_class = ConceptExpression("TempSubClass")
            temp_super_class = ConceptExpression("TempSuperClass")
            
            self.add_axiom(RightTerminology(temp_sub_class, axiom.left))
            self.add_axiom(LeftTerminology(axiom.right, temp_super_class))
            
            sync_reasoner(self.ontology)
            
            entails = self.ontology[temp_super_class.name] in self.ontology[temp_sub_class.name].ancestors() # type: ignore[ancestors]
            
            with self.ontology:
                owlready2.destroy_entity(self.ontology[temp_super_class.name])
                owlready2.destroy_entity(self.ontology[temp_sub_class.name])
            
            return entails
        
        # Creates one new concept expression to check if it is correct
        entails: bool = False
        temp_class = ConceptExpression("TempClass")
        if isinstance(axiom, RightTerminology):    
            self.add_axiom(LeftTerminology(axiom.right,temp_class))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.left.name]
            
            if b != None:
                entails = self.ontology[temp_class.name] in b.ancestors() # type: ignore[ancestors]
        elif isinstance(axiom, LeftTerminology):
            self.add_axiom(RightTerminology(temp_class,axiom.left))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.right.name]
            
            if b != None:
                entails = b in self.ontology[temp_class.name].ancestors() # type: ignore[ancestors]
        with self.ontology:
            owlready2.destroy_entity(self.ontology[temp_class.name])
        return entails
    
    def add_axiom(self, axiom: RightTerminology | LeftTerminology):
        """Adds an axiom to the engines ontology. If there is a terminology with that given concept, it gets overwritten.

        Args:
            axiom (RightTerminology | LeftTerminology): Axiom to be added
        """
        if isinstance(axiom, LeftTerminology):
            # Checks if it is better as a right terminology. This has to do with the way owlready2 works.
            if len(axiom.left.labels) == 1 and len(axiom.left.edges) == 0:
                axiom = RightTerminology(axiom.left.labels[0], Node([axiom.right],[]))
            else:
                complex_expression = self._node_convert(axiom.left)
                concept_expression = self._concept_convert(axiom.right)
                with self.ontology:
                    gca = GeneralClassAxiom(complex_expression)
                    gca.is_a.append(concept_expression) # type: ignore[is_a]
        if isinstance(axiom, RightTerminology):
            complex_expression = self._node_convert(axiom.right)
            concept_expression = self._concept_convert(axiom.left)
            with self.ontology:
                concept_expression.is_a.append(complex_expression) # type: ignore[is_a]
        self.ontology_list.add_axiom(axiom)
        
    def get_hypothesis(self) -> List[RightTerminology | LeftTerminology]:
        """Get the ontology in form of axioms

        Returns:
            List[Right | Left]: The ontology as a list of axioms
        """
        return self.ontology_list.get_list()
    
    def _node_convert(self, node: Node) -> ThingClass | ObjectPropertyClass | And:
        """Converts a Node object into something that owlready2 can handle

        Args:
            node (Node): input

        Returns:
            ThingClass | ObjectPropertyClass | And: returns in owlready2 form
        """
        # If the node doesn't have any children or labels, it is considered to be ⊤
        if len(node.labels) == 0 and len(node.edges) == 0:
            return Thing
        
        a: List[ThingClass | ObjectPropertyClass] = [self._concept_convert(c) for c in node.labels]
        a.extend([self._edge_convert(c) for c in node.edges])
        
        if len(a) <= 1:
            return a[0]
        
        return And(a)
    
    def _concept_convert(self, concept: ConceptExpression) -> ThingClass:
        """Converts a concept expression into owlready2 form. If the concept does not exist in
        the ontology, it is added.

        Args:
            concept (ConceptExpression): input concept

        Returns:
            ThingClass: returned class.
        """
        with self.ontology:
            c = self.ontology[concept.name]
            if c == None:
                c= types.new_class(concept.name, (Thing, ))
            return c
    
    def _edge_convert(self, edge: Edge) -> ObjectPropertyClass: # Not correct type i think.
        with self.ontology:
            c = self.ontology[edge.label.name]
            if c == None:
                c = types.new_class(edge.label.name, (ObjectProperty, ))
            return c.some(self._node_convert(edge.target))
    
    def get_right_from_hypothesis(self, concept_expression: ConceptExpression) -> RightTerminology | None:
        if concept_expression not in self.ontology_list.right_map:
            return None
        return self.ontology_list.right_map[concept_expression]
