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

    def add_entity(self, entity):
        self.entities[entity.id] = entity

    def add_system(self, system):
        self.systems.append(system)

    def update(self):
        """Fait tourner chaque système l'un après l'autre."""
        for system in self.systems:
            system.update(self.entities, self.world_state)
