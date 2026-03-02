from components.base import ActionRequest


class HungerSystem:
    def update(self, entities, world_state):


        for entity in entities:
            e = entities[entity]
            if e.get_comp("Dead"): continue

            hunger = e.get_comp("Hunger")
            if not hunger:
                continue
            if world_state.get("new_hour_pulse"):
                hunger.current -= 1

            if hunger.current <= hunger.threshold:
                if not e.get_comp("ActionRequest"):
                    e.add_comp(ActionRequest("EAT_FOOD", 10))
            
            if hunger.current <= 0:
                hunger.current = 0