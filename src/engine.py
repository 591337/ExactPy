from owlready2 import Ontology, And, GeneralClassAxiom, ObjectProperty, Thing, sync_reasoner, get_ontology
import owlready2
from src.dataclass import *
import types
owlready2.JAVA_EXE = "C:\\Users\\marti\\.jdks\\openjdk-17.0.2\\bin\\java.exe"


class OwlEngine:
    
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
    
    def entails(self, axiom: Right | Left) -> bool:
        if isinstance(axiom, Right):    
            temp_class = Class("TempClass")
            
            self.addAxiom(Left(axiom.right, temp_class))
            
            sync_reasoner(self.ontology)
                                    
            b = self.ontology[axiom.left.name]
            
            entailes = self.ontology[temp_class.name] in b.is_a # type: ignore[is_a]
            
            with self.ontology:
                owlready2.destroy_entity(self.ontology[temp_class.name])
            
            return entailes
        else:
            temp_class = Class("TempClass")
            
            self.addAxiom(Right(temp_class,axiom.left))
            
            sync_reasoner(self.ontology)
                                    
            b = self.ontology[axiom.right.name]
            
            entailes = b in self.ontology[temp_class.name].is_a # type: ignore[is_a]
            
            with self.ontology:
                owlready2.destroy_entity(self.ontology[temp_class.name])
            
            return entailes
            
        return False
        
        
        
    
    def addAxiom(self, axiom: Right | Left):
        if isinstance(axiom, Left):
            ax = self._node_convert(axiom.left)
            c = self._val_convert(axiom.right)
            with self.ontology:
                gca = GeneralClassAxiom(ax)
                gca.is_a.append(c) # type: ignore[is_a]
        elif isinstance(axiom, Right):
            ax = self._node_convert(axiom.right)
            c = self._val_convert(axiom.left)
            with self.ontology:
                c.is_a.append(ax)
    
    def _node_convert(self, node: Node):
        if len(node.inf) == 0:
            return Thing
        elif len(node.inf) == 1:
            return self._val_convert(node.inf[0])
        else:
            return And(self._val_convert(n) for n in node.inf)
            
    
    def _val_convert(self, rc: Relation | Class):
        with self.ontology:
            if isinstance(rc, Class):
                c = self.ontology[rc.name]
                if c == None:
                    c = types.new_class(rc.name, (Thing, ))
                return c
            else:
                c = self.ontology[rc.name]
                if c == None:
                    c = types.new_class(rc.name, (ObjectProperty, ))
                return c.some(self._node_convert(rc.node))
