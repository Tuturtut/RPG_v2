import unicodedata


class ContextTagBuilder:

    def build(self, entity, world_state):

        tags = set(entity.tags)

        if not entity.has_comp("Dead"):
            tags.add("alive")

        if entity.has_comp("Area"):
            tags.add("area")

        if isinstance(entity.id, str):
            tags.add(entity.id)

        tags.add(f"entity_{self.slug(entity.name)}")

        self.add_time_tags(tags, world_state)
        self.add_world_tags(tags, world_state)
        self.add_actor_tags(tags, entity)
        self.add_location_tags(tags, entity, world_state)
        self.add_goal_tags(tags, entity)

        return tags

    def add_time_tags(self, tags, world_state):

        engine = world_state.get("engine")
        clock = engine.get_comp("GameClock") if engine else None

        if not clock:
            return

        if clock.hours < 6 or clock.hours >= 20:
            tags.add("night")

        elif 6 <= clock.hours < 12:
            tags.add("morning")

        elif 12 <= clock.hours < 18:
            tags.add("afternoon")

        else:
            tags.add("evening")

    def add_world_tags(self, tags, world_state):

        if world_state.get("is_raining"):
            tags.add("rain")
        else:
            tags.add("dry_weather")

        if world_state.get("war_declared"):
            tags.add("war")

        if world_state.get("combat_active"):
            tags.add("combat")

        if world_state.get("tavern_open"):
            tags.add("tavern_open")
        else:
            tags.add("tavern_closed")

        for event_tag in world_state.get("event_tags", []):
            tags.add(event_tag)

    def add_actor_tags(self, tags, entity):

        mood = entity.get_comp("Mood")
        if mood:
            tags.add(f"mood_{self.slug(mood.feeling)}")

        mindset = entity.get_comp("Mindset")
        if mindset:
            tags.add(f"mindset_{self.slug(mindset.trait)}")

        hunger = entity.get_comp("Hunger")
        if hunger:
            if hunger.current <= 0:
                tags.add("starving")
            elif hunger.current <= hunger.threshold:
                tags.add("hungry")
            elif hunger.current >= hunger.max_val:
                tags.add("full")

        health = entity.get_comp("Health")
        health_current = None
        health_max = None

        if health:
            health_current = getattr(
                health,
                "current",
                getattr(health, "current_health", None)
            )
            health_max = getattr(
                health,
                "max_val",
                getattr(health, "max_health", None)
            )

        if health_current is not None and health_max is not None:
            if health_current < health_max:
                tags.add("wounded")

    def add_location_tags(self, tags, entity, world_state):

        position = entity.get_comp("Position")
        world = world_state.get("world")
        location = None

        if position and world:
            location = world.entities.get(position.at_entity_id)

        if not location:
            return

        tags.update(location.tags)

        if isinstance(location.id, str):
            tags.add(location.id)

        tags.add(f"location_{self.slug(location.name)}")

    def add_goal_tags(self, tags, entity):
        goal = entity.get_comp("Goal")
        if goal:
            goal_value = getattr(goal, "value", None)
            if goal_value:
                tags.add(f"goal_{self.slug(goal_value)}")

        movement = entity.get_comp("Movement")
        if movement:
            tags.add("moving")
            tags.add(f"moving_to_{self.slug(movement.target_entity_id)}")

    def tags_match(self, required_tags, forbidden_tags, context_tags):

        context_tags = set(context_tags)
        return (
            set(required_tags).issubset(context_tags)
            and set(forbidden_tags).isdisjoint(context_tags)
        )

    def slug(self, value):

        value = str(value).strip().lower().replace(" ", "_")
        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("ascii")

        return "".join(
            char for char in value
            if char.isalnum() or char == "_"
        )
