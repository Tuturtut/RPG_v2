class MovementSystem:
    def update(self, entities, world_state):
        for entity in entities:
            e = entities[entity]
            if e.get_comp("Dead"): continue

            movement = e.get_comp("Movement")
            if not movement:
                continue

            pos = e.get_comp("Position")
            if not pos:
                continue

            pos.location_name = movement.direction.name
            pos.at_entity = movement.direction

            e.remove_comp("Movement")