from typing import List
from owlready2 import Ontology, And, GeneralClassAxiom, ObjectProperty, Thing, sync_reasoner, get_ontology
import owlready2
from src.dataclass import Left, Right
import types
owlready2.JAVA_EXE = "C:\\Users\\marti\\.jdks\\openjdk-17.0.2\\bin\\java.exe"

from src.protocols import Consept, Role, Expression

class OwlEngine:
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology_list: List[Left | Right] = []
    
    def entails(self, axiom: Left | Right) -> bool:
        entailes: bool = False
        temp_class = Consept("TempClass")
        if isinstance(axiom, Left):    
            self.add_axiom(Right(axiom.right,temp_class))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.left.name]
            
            entailes = self.ontology[temp_class.name] in b.ancestors() # type: ignore[ancestors]
        else:
            self.add_axiom(Left(temp_class,axiom.left))
            
            sync_reasoner(self.ontology)                 
            b = self.ontology[axiom.right.name]
            
            entailes = b in self.ontology[temp_class.name].ancestors() # type: ignore[ancestors]

        with self.ontology:
            owlready2.destroy_entity(self.ontology[temp_class.name])
        return entailes
    
    def add_axiom(self, axiom: Left | Right):
        if isinstance(axiom, Right):
            if len(axiom.left.inf) == 1 and isinstance(axiom.left.inf[0], Consept):
                axiom = Left(axiom.left.inf[0], Expression([axiom.right]))
            else:
                ax = self._node_convert(axiom.left)
                c = self._val_convert(axiom.right)
                with self.ontology:
                    gca = GeneralClassAxiom(ax)
                    gca.is_a.append(c) # type: ignore[is_a]
        if isinstance(axiom, Left):
            ax = self._node_convert(axiom.right)
            c = self._val_convert(axiom.left)
            with self.ontology:
                c.is_a.append(ax)
        self.ontology_list.append(axiom)
    
    def get_hypothisis(self) -> List[Left | Right]:
        return self.ontology_list
    
    def _node_convert(self, node: Expression):
        if len(node.inf) == 0:
            return Thing
        elif len(node.inf) == 1:
            return self._val_convert(node.inf[0])
        else:
            return And(self._val_convert(n) for n in node.inf)
            
    
    def _val_convert(self, rc: Role | Consept):
        with self.ontology:
            if isinstance(rc, Consept):
                c = self.ontology[rc.name]
                if c == None:
                    c = types.new_class(rc.name, (Thing, ))
                return c
            else:
                c = self.ontology[rc.name]
                if c == None:
                    c = types.new_class(rc.name, (ObjectProperty, ))
                return c.some(self._node_convert(rc.expression))
