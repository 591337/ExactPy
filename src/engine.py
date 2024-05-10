from typing import Any, List
from owlready2 import Ontology, And, GeneralClassAxiom, ObjectProperty, Thing, sync_reasoner, get_ontology
import owlready2
from src.dataclass import Right, Left
import types
owlready2.JAVA_EXE = "C:\\Users\\marti\\.jdks\\openjdk-17.0.2\\bin\\java.exe"

from src.protocols import Consept, Role, Expression, InclutionAxiom

class OwlEngine:
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology_list: List[Right | Left] = []
    
    def entails(self, axiom: Right | Left | InclutionAxiom) -> bool:
        if isinstance(axiom, InclutionAxiom):
            temp_sub_class = Consept("TempSubClass")
            temp_super_class = Consept("TempSuperClass")
            
            self.add_axiom(Right(temp_sub_class, axiom.left))
            self.add_axiom(Left(axiom.right, temp_super_class))
            
            sync_reasoner(self.ontology)
            
            entailes = self.ontology[temp_super_class.name] in self.ontology[temp_sub_class.name].ancestors() # type: ignore[ancestors]
            
            with self.ontology:
                owlready2.destroy_entity(self.ontology[temp_super_class.name])
                owlready2.destroy_entity(self.ontology[temp_sub_class.name])
            
            return entailes
        
        entailes: bool = False
        temp_class = Consept("TempClass")
        if isinstance(axiom, Right):    
            self.add_axiom(Left(axiom.right,temp_class))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.left.name]
            
            entailes = self.ontology[temp_class.name] in b.ancestors() # type: ignore[ancestors]
        elif isinstance(axiom, Left):
            self.add_axiom(Right(temp_class,axiom.left))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.right.name]
            
            entailes = b in self.ontology[temp_class.name].ancestors() # type: ignore[ancestors]
        with self.ontology:
            owlready2.destroy_entity(self.ontology[temp_class.name])
        return entailes
    
    def add_axiom(self, axiom: Right | Left):
        if isinstance(axiom, Left):
            if len(axiom.left.consepts) == 1 and len(axiom.left.roles) == 0:
                axiom = Right(axiom.left.consepts[0], Expression([axiom.right],[]))
            else:
                ax = self._node_convert(axiom.left)
                c = self._consept_convert(axiom.right)
                with self.ontology:
                    gca = GeneralClassAxiom(ax)
                    gca.is_a.append(c) # type: ignore[is_a]
        if isinstance(axiom, Right):
            ax = self._node_convert(axiom.right)
            c = self._consept_convert(axiom.left)
            with self.ontology:
                c.is_a.append(ax)
        self.ontology_list.append(axiom)
    
    def get_hypothisis(self) -> List[Right | Left]:
        return self.ontology_list
    
    def _node_convert(self, node: Expression):
        if len(node.consepts) == 0 and len(node.roles) == 0:
            return Thing
        
        a = [self._consept_convert(c) for c in node.consepts]
        a.extend([self._role_convert(c) for c in node.roles])
        
        if len(a) <= 1:
            return a[0]
        
        return And(a)
    
    def _consept_convert(self, consept: Consept) -> Any:
        with self.ontology:
            c = self.ontology[consept.name]
            if c == None:
                c= types.new_class(consept.name, (Thing, ))
            return c
    
    def _role_convert(self, role: Role) -> Any:
        with self.ontology:
            c = self.ontology[role.name]
            if c == None:
                c = types.new_class(role.name, (ObjectProperty, ))
            return c.some(self._node_convert(role.expression))
