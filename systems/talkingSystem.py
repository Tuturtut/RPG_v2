import random

from systems.contextTagBuilder import ContextTagBuilder
from templates.narrative_templates import DIALOGUES


class TalkingSystem:

    def __init__(
        self,
        talk_chance=0.3,
        reply_chance=0.3,
        dialogues=None,
        context_builder=None
    ):
        self.talk_chance = talk_chance
        self.reply_chance = reply_chance
        self.dialogues = dialogues or DIALOGUES
        self.context_builder = context_builder or ContextTagBuilder()

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
        return self.context_builder.build(entity, world_state)

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
        return self.context_builder.tags_match(
            required_tags,
            forbidden_tags,
            context_tags
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
        return self.context_builder.slug(value)
