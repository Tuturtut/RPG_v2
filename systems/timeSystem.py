class TimeSystem:
    def update(self, entities, world_state):
        clock_entity = next((e for e in entities if e.has_comp("GameClock")), None)
        if not clock_entity: return

        clock = clock_entity.get_comp("GameClock")
        
        clock.tick += 1
        clock.minutes += 10

        if clock.minutes >= 60:
            clock.hours += 1
            clock.minutes = 0
        
        if clock.hours >= 24:
            clock.days += 1
            clock.hours = 0

            world_state["logs"].append(f"Jour {clock.days}")