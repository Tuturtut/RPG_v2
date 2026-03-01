class TimeSystem:
    def update(self, entities, world_state):

        engine = world_state["engine"]
        if not engine: return

        clock = engine.get_comp("GameClock")

        last_hour = world_state.get("last_hour", clock.hours - 1)

        world_state["new_hour_pulse"] = False
        world_state["new_day_pulse"] = False

        if clock.hours != last_hour:
            world_state["new_hour_pulse"] = True
            world_state["last_hour"] = clock.hours
        
            if clock.hours == 0:
                world_state["new_day_pulse"] = True
        
        clock.tick += 1
        clock.minutes += 10

        if clock.minutes >= 60:
            clock.hours += 1
            clock.minutes = 0
        
        if clock.hours >= 24:
            clock.days += 1
            clock.hours = 0

            world_state["logs"].append(f"Jour {clock.days}")