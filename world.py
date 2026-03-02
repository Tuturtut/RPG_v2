from entity import Entity


class World:
    """Le chef d'orchestre qui contient les entités et fait tourner les systèmes."""
    def __init__(self):
        self.entities = {}
        self.systems = []
        self.world_state = {
            "is_raining": False,
            "war_declared": False,
            "world": self,
            "tick": 0,
            "chronicles": [],
            "logs": []
        }
    
    def create_entity(self, id, name):
        new_entity = Entity(id, name)
        self.entities[id] = new_entity
        return id
    
    def add_comp(self, entity_id, component):
        entity = self.entities.get(entity_id)
        if entity:
            comp_name = type(component).__name__
            entity.components[comp_name] = component
        return self

    def get_comp(self, entity_id, component_name):
        entity = self.entities.get(entity_id)
        if entity:
            return entity.components.get(component_name)
        return None
    
    def has_comp(self, entity_id, component_name):
        entity = self.entities.get(entity_id)
        return component_name in entity.components if entity else False

    def remove_entity(self, entity_id):
        self.entities.pop(entity_id, None)
    
    def add_tag(self, entity_id, tag_name):
        entity = self.entities.get(entity_id)
        if entity:
            entity.tags.add(tag_name)
    
    def remove_tag(self, entity_id, tag_name):
        entity = self.entities.get(entity_id)
        if entity:
            entity.tags.remove(tag_name)

    def add_system(self, system):
        self.systems.append(system)

    def update(self):
        """Fait tourner chaque système l'un après l'autre."""
        for system in self.systems:
            system.update(self.entities, self.world_state)
