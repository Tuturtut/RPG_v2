from components.base import Movement

class GoalResolutionSystem:
    GOAL_TARGETS = {
        "walk_in_forest": "forest",
        "rest": "tavern",
    }

    def update(self, entities, world_state):
        for entity_id, e in entities.items():
            if e.has_comp("Dead"):
                continue

            goal = e.get_comp("Goal")
            if not goal:
                continue

            pos = e.get_comp("Position")
            if not pos:
                continue

            target_id = self.GOAL_TARGETS.get(goal.value)
            if not target_id:
                continue

            target = entities.get(target_id)
            if not target or not target.has_comp("Area"):
                continue

            if pos.at_entity_id != target_id:
                e.add_comp(Movement(target_entity_id=target_id))

            e.remove_comp("Goal")