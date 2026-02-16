from components.base import ActionRequest


class HungerSystem:
    def update(self, entities, world_state):
        for e in entities:
            hunger = e.get_comp("Hunger")
            if not hunger:
                continue

            hunger.current -= 1

            if hunger.current <= hunger.threshold:
                if not e.get_comp("ActionRequest"):
                    e.add_comp(ActionRequest("EAT_FOOD", 10))