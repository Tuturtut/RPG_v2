import random

from components.base import Delete

class EatingSystem:
    def update(self, entities, world_state):

        shuffled_entities = list(entities)
        random.shuffle(shuffled_entities)

        for entity in shuffled_entities:
            e = entities[entity]
            action = e.get_comp("ActionRequest")
            hunger = e.get_comp("Hunger")
            inv = e.get_comp("Inventory")
            pos = e.get_comp("Position")

            if e.get_comp("Dead"): continue

            if not (action and hunger):
                continue

            if action and action.type == "EAT_FOOD":
                item_to_eat = None
                if pos and pos.at_entity_id:
                    for i in entities:
                        item = entities[i]
                        item_data = item.get_comp("Item")
                        item_pos = item.get_comp("Position")
                        

                        if not item_data: continue
                        if not item_pos: continue

                        if item.get_comp("Position").at_entity_id == pos.at_entity_id:
                            if item.has_comp("Delete"): continue

                            item_data = item.get_comp("Item")
                            if item_data:
                                if item_data.type == "FOOD":

                                    item_to_eat = item
                                    break

                if not item_to_eat and inv: 
                    for item in inv.items:
                        item_data = item.get_comp("Item")
                        if item_data and item_data.type == "food":
                            item_to_eat = item
                            break

                if item_to_eat:
                    hunger.current = hunger.max_val
                    e.remove_comp("ActionRequest")
                    item_to_eat.add_comp(Delete())
                    