import random
import unicodedata

from templates.narrative_templates import DIALOGUES


class TalkingSystem:

    def __init__(self, talk_chance=0.3, reply_chance=0.3, dialogues=None):
        self.talk_chance = talk_chance
        self.reply_chance = reply_chance
        self.dialogues = dialogues or DIALOGUES

    def update(self, entities, world_state):

        chronicles = world_state.setdefault("chronicles", [])
        speakers = list(entities.values())
        random.shuffle(speakers)

        for entity in speakers:

            if not self.can_talk(entity):
                continue

            if random.random() > self.talk_chance:
                continue

            context_tags = self.build_context_tags(entity, world_state)

            sentence = self.get_random_dialogue(
                entity.name,
                "talk",
                context_tags
            )

            if sentence is None:
                continue

            chronicles.append(
                f"{entity.name} says:\n - {sentence}"
            )

            self.handle_replies(
                speaker=entity,
                entities=entities,
                chronicles=chronicles,
                world_state=world_state
            )

            break

    def can_talk(self, entity):

        if entity.has_comp("Dead"):
            return False

        if not entity.has_comp("Position"):
            return False

        if not entity.has_comp("Health"):
            return False

        return True

    def build_context_tags(self, entity, world_state):

        tags = set(entity.tags)
        tags.add("alive")

        self.add_time_tags(tags, world_state)
        self.add_world_tags(tags, world_state)
        self.add_actor_tags(tags, entity)
        self.add_location_tags(tags, entity, world_state)

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

        if world_state.get("new_hour_pulse"):
            tags.add("new_hour")

        if world_state.get("new_day_pulse"):
            tags.add("new_day")

    def add_world_tags(self, tags, world_state):

        if world_state.get("is_raining"):
            tags.add("rain")
        else:
            tags.add("dry_weather")

        if world_state.get("war_declared"):
            tags.add("war")

        if world_state.get("combat_active"):
            tags.add("combat")

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

        if location:
            tags.update(location.tags)

            if isinstance(location.id, str):
                tags.add(location.id)

            tags.add(f"location_{self.slug(location.name)}")

    def get_random_dialogue(
        self,
        entity_name,
        dialogue_type,
        context_tags
    ):

        valid_dialogues = self.find_valid_dialogues(
            entity_name,
            dialogue_type,
            context_tags
        )

        if not valid_dialogues:
            return None

        chosen_dialogue = random.choice(valid_dialogues)

        return random.choice(chosen_dialogue["texts"])

    def find_valid_dialogues(
        self,
        entity_name,
        dialogue_type,
        context_tags
    ):

        entity_dialogues = self.dialogues.get(entity_name, {})
        valid_dialogues = []

        for dialogue in entity_dialogues.get(dialogue_type, []):

            required_tags = dialogue.get("required_tags", [])
            forbidden_tags = dialogue.get("forbidden_tags", [])

            if not self.tags_match(
                required_tags,
                forbidden_tags,
                context_tags
            ):
                continue

            valid_dialogues.append(dialogue)

        return valid_dialogues

    def tags_match(
        self,
        required_tags,
        forbidden_tags,
        context_tags
    ):

        context_tags = set(context_tags)
        return (
            set(required_tags).issubset(context_tags)
            and set(forbidden_tags).isdisjoint(context_tags)
        )

    def handle_replies(
        self,
        speaker,
        entities,
        chronicles,
        world_state
    ):

        speaker_position = speaker.get_comp("Position")

        for other in entities.values():

            if other.id == speaker.id:
                continue

            if not self.can_talk(other):
                continue

            other_position = other.get_comp("Position")

            if other_position.at_entity_id != speaker_position.at_entity_id:
                continue

            if random.random() > self.reply_chance:
                continue

            reply_context_tags = self.build_context_tags(other, world_state)
            reply_context_tags.add("reply")
            reply_context_tags.add(f"speaker_{self.slug(speaker.name)}")

            reply = self.get_random_dialogue(
                other.name,
                "reply",
                reply_context_tags
            )

            if reply is None:
                continue

            chronicles.append(
                f"{other.name} replies:\n - {reply}"
            )

    def slug(self, value):

        value = str(value).strip().lower().replace(" ", "_")
        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("ascii")

        return "".join(
            char for char in value
            if char.isalnum() or char == "_"
        )
