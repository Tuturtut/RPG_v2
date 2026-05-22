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

            for task_time, task_name in schedule.tasks:
                if current_hour >= task_time:
                    schedule.current_task_index = schedule.tasks.index((task_time, task_name))