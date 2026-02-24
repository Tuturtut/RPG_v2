from components.biology import Dead

class HealthSystem:
    def update(self, entities, world_state):
        for e in entities:
            health = e.get_comp("Health")
            if not health:
                continue

            hunger = e.get_comp("Hunger")
            if hunger and hunger.current == 0:
                health.current_health -= 1
            
            if health.current_health <= 0:
                health.current_health = 0
                if not e.get_comp("Dead"):
                    e.add_comp(Dead())