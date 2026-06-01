from components.base import Goal

class ScheduleSystem:
    def update(self, entities, world_state):
        for entity_id, e in entities.items():
            if e.has_comp("Dead"):
               continue

            schedule = e.get_comp("Schedule")
            if not schedule:
                continue

            game_clock = world_state.get("engine").get_comp("GameClock")
            _, hours, minutes = game_clock.get_time()


            # 1. Action ponctuelle
            actions = schedule.get_actions_for_time(hours=hours, minutes=minutes)
            for action in actions:
                world_state["chronicles"].append(f"{e.name} performs action: {action}")
                e.add_comp(Goal(action))

            # 2. Activité de longue durée
            activity = schedule.get_current_activity(hours=hours, minutes=minutes)


            if not activity:
                continue

            current_goal = e.get_comp("Goal")
            if current_goal and current_goal.value == activity:
                continue

            e.add_comp(Goal(activity))