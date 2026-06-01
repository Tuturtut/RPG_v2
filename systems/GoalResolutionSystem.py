from components.base import Movement

class GoalResolutionSystem:
    GOAL_TARGETS = {
        "walk_in_forest": "forest",
        "rest": "tavern",
        "train": "training_ground",
        "open_tavern": "tavern",
        "close_tavern": "tavern",
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

            # Differents steps to resolve the goal:
            # 1. Does the target need to go somewhere else?
            if pos.at_entity_id != target_id:
                if not e.has_comp("Movement"):
                    e.add_comp(Movement(target_entity_id=target_id))
                continue

            # 2. If the target has reached the area, resolve the goal
            if goal.value == "open_tavern":
                world_state["tavern_open"] = True
            
            if goal.value == "close_tavern":
                world_state["tavern_open"] = False

            e.remove_comp("Goal")