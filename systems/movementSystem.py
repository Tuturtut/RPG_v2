class MovementSystem:
    def update(self, entities, world_state):
        for entity_id, e in entities.items():
            if e.get_comp("Dead"): continue

            movement = e.get_comp("Movement")
            if not movement:
                continue

            pos = e.get_comp("Position")
            if not pos:
                continue

            target_id = movement.target_entity_id
            target = entities.get(target_id)

            if not target:
                world_state.setdefault("logs", []).append(
                    f"{e.name} ne peut pas se deplacer vers une cible inconnue: {target_id}"
                )
                e.remove_comp("Movement")
                continue

            pos.at_entity_id = target_id

            e.remove_comp("Movement")
