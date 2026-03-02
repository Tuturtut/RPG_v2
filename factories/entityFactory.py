from entity import Entity
from components.base import Position
from components.biology import Hunger, Health, Mindset
from components.economy import Item

class EntityFactory:
    def __init__(self, world_state):
        self.world_state = world_state

    def create_item(self, name, item_type):
        """Crée un objet physique (comme du pain)."""
        item_ent = Entity(name, id=name+"_"+item_type+"_"+str(len(self.world_state["world"].entities)))
        # On ajoute les composants de base pour un objet
        item_ent.add_comp(Item(type=item_type))
        # On ne met pas de Position ici, on laisse le Director s'en charger 
        # car il sait OÙ le pain tombe.
        return item_ent

    def create_prisoner(self, name, trait):
        """Crée un humain avec des stats de base."""
        p = Entity(name)
        p.add_comp(Health(max_health=10, current_health=10))
        p.add_comp(Hunger(max_val=10, current=5)) # Commence à moitié faim
        p.add_comp(Mindset(trait=trait))
        p.add_comp(Position(location_name="Cellule"))
        return p