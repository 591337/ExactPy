from dataclasses import dataclass
from typing import Any, Dict, List
from owlready2 import Ontology, And, GeneralClassAxiom, ObjectProperty, Thing, sync_reasoner, get_ontology
import owlready2
from src.data.special import Right, Left
import types
owlready2.JAVA_EXE = "C:\\Users\\marti\\.jdks\\openjdk-17.0.2\\bin\\java.exe"

from src.data.communication import Concept, Role, Expression, InclutionAxiom

@dataclass
class OntologyMap:
    left_map: Dict[Concept, Left]
    right_map: Dict[Concept, Right]
    other: List[InclutionAxiom]
    
    def add_axiom(self, axiom: Left | Right | InclutionAxiom) -> None:
        if isinstance(axiom, Left):
            self.left_map[axiom.right] = axiom
        elif isinstance(axiom, Right):
            self.right_map[axiom.left] = axiom
    
    def get_list(self) -> List[Left | Right]:
        l: List[Left | Right] = list(self.left_map.values())
        l.extend(self.right_map.values())
        return l
    
class OwlEngine:
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology_list: OntologyMap = OntologyMap({}, {}, [])
    
    def entails(self, axiom: Right | Left | InclutionAxiom) -> bool:
        if isinstance(axiom, InclutionAxiom):
            temp_sub_class = Concept("TempSubClass")
            temp_super_class = Concept("TempSuperClass")
            
            self.add_axiom(Right(temp_sub_class, axiom.left))
            self.add_axiom(Left(axiom.right, temp_super_class))
            
            sync_reasoner(self.ontology)
            
            entailes = self.ontology[temp_super_class.name] in self.ontology[temp_sub_class.name].ancestors() # type: ignore[ancestors]
            
            with self.ontology:
                owlready2.destroy_entity(self.ontology[temp_super_class.name])
                owlready2.destroy_entity(self.ontology[temp_sub_class.name])
            
            return entailes
        
        entailes: bool = False
        temp_class = Concept("TempClass")
        if isinstance(axiom, Right):    
            self.add_axiom(Left(axiom.right,temp_class))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.left.name]
            
            if b != None:
                entailes = self.ontology[temp_class.name] in b.ancestors() # type: ignore[ancestors]
        elif isinstance(axiom, Left):
            self.add_axiom(Right(temp_class,axiom.left))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.right.name]
            
            if b != None:
                entailes = b in self.ontology[temp_class.name].ancestors() # type: ignore[ancestors]
        with self.ontology:
            owlready2.destroy_entity(self.ontology[temp_class.name])
        return entailes
    
    def add_axiom(self, axiom: Right | Left):
        if isinstance(axiom, Left):
            if len(axiom.left.concepts) == 1 and len(axiom.left.roles) == 0:
                axiom = Right(axiom.left.concepts[0], Expression([axiom.right],[]))
            else:
                ax = self._node_convert(axiom.left)
                c = self._concept_convert(axiom.right)
                with self.ontology:
                    gca = GeneralClassAxiom(ax)
                    gca.is_a.append(c) # type: ignore[is_a]
        if isinstance(axiom, Right):
            ax = self._node_convert(axiom.right)
            c = self._concept_convert(axiom.left)
            with self.ontology:
                c.is_a.append(ax)
        self.ontology_list.add_axiom(axiom)
        
    def get_hypothisis(self) -> List[Right | Left]:
        return self.ontology_list.get_list()
    
    def _node_convert(self, node: Expression):
        if len(node.concepts) == 0 and len(node.roles) == 0:
            return Thing
        
        a = [self._concept_convert(c) for c in node.concepts]
        a.extend([self._role_convert(c) for c in node.roles])
        
        if len(a) <= 1:
            return a[0]
        
        return And(a)
    
    def _concept_convert(self, concept: Concept) -> Any:
        with self.ontology:
            c = self.ontology[concept.name]
            if c == None:
                c= types.new_class(concept.name, (Thing, ))
            return c
    
    def _role_convert(self, role: Role) -> Any:
        with self.ontology:
            c = self.ontology[role.name]
            if c == None:
                c = types.new_class(role.name, (ObjectProperty, ))
            return c.some(self._node_convert(role.expression))
    
    def get_right_from_hypothisis(self, concept: Concept) -> Right | None:
        if concept not in self.ontology_list.right_map:
            return None
        return self.ontology_list.right_map[concept]
