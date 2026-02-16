class DeleteSystem:
    def update(self, entities, world_state):
        for e in entities:
            if e.get_comp("Delete"):
                entities.remove(e)