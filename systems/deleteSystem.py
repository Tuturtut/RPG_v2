class DeleteSystem:
    def update(self, entities, world_state):
        to_delete = []

        for entity in entities:
            e = entities[entity]
            if e.get_comp("Delete"):
                to_delete.append(entity)
        
        for entity in to_delete:
            entities.pop(entity, None)