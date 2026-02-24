class PrisonAISystem:
    def update(self, entities, world_state):
        foods = [e for e in entities if e.get_comp("Item") and e.get_comp("Item").type == "food" and e.has_comp("Position")]

        for e in entities:
            if not e.get_comp("Hunger") or e.get_comp("Dead"): continue

            if foods:
                target_bread = foods[0]
                e.add_comp