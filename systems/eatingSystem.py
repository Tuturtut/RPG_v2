class EatingSystem:
    def update(self, entities, world_state):
        for e in entities:
            action = e.get_comp("ActionRequest")
            hunger = e.get_comp("Hunger")
            inv = e.get_comp("Inventory")

            if action and action.type == "EAT_FOOD":
                if "Biere" in inv.items:
                    inv.items.remove("Biere")
                    hunger.current = hunger.max_val

                    e.remove_comp("ActionRequest")
                    