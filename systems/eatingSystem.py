from components.base import Delete

class EatingSystem:
    def update(self, entities, world_state):
        for e in entities:
            action = e.get_comp("ActionRequest")
            hunger = e.get_comp("Hunger")
            inv = e.get_comp("Inventory")

            if not (action and hunger and inv):
                continue

            if action and action.type == "EAT_FOOD":
                item_to_eat = None

                for item in inv.items:
                    item_data = item.get_comp("Item")
                    if item_data and item_data.type == "food":
                        item_to_eat = item
                        break
                
                if item_to_eat:
                    inv.items.remove(item_to_eat)        
                    hunger.current = hunger.max_val
                    e.remove_comp("ActionRequest")
                    item_to_eat.add_comp(Delete())
                    