from components.base import Delete

class EatingSystem:
    def update(self, entities, world_state):
        for e in entities:
            action = e.get_comp("ActionRequest")
            hunger = e.get_comp("Hunger")
            inv = e.get_comp("Inventory")
            pos = e.get_comp("Position")

            if not (action and hunger):
                continue

            if action and action.type == "EAT_FOOD":
                item_to_eat = None
            
                if pos and pos.at_entity:
                    for item in entities:
                        item_data = item.get_comp("Item")
                        item_pos = item.get_comp("Position")

                        if not item_data: continue
                        if not item_pos: continue

                        if item.get_comp("Position").at_entity == pos.at_entity:

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
                    