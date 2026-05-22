from components.base import Goal

class ScheduleSystem:
    def update(self, entities, world_state):
        for entity_id, e in entities.items():
            if e.has_comp("Dead"):
               continue

            if not e.has_comp("Schedule"):
                continue
            schedule = e.get_comp("Schedule")
            game_clock = world_state.get("engine").get_comp("GameClock")

            current_hour = game_clock.hours

            activity = schedule.get_current_activity(current_hour)
            if not activity:
                continue

            current_goal = e.get_comp("Goal")
            if current_goal and current_goal.value == activity:
                continue

            e.add_comp(Goal(activity))