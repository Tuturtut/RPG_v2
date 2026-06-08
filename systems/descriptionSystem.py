import random

from systems.contextTagBuilder import ContextTagBuilder
from templates.narrative_templates import DESCRIPTIONS


class DescriptionSystem:

    def __init__(
        self,
        description_chance=0.2,
        descriptions=None,
        context_builder=None
    ):
        self.description_chance = description_chance
        self.descriptions = descriptions or DESCRIPTIONS
        self.context_builder = context_builder or ContextTagBuilder()

    def update(self, entities, world_state):
        player = world_state.get("player")
        if not player:
            return
        players_current_position = player.get_comp("Position") if player and player.has_comp("Position") else None
        if not players_current_position:
            return

        chronicles = world_state.setdefault("chronicles", [])
        describable_entities = [
            entity for entity in entities.values()
            if self.can_describe(entity)
        ]
        random.shuffle(describable_entities)

        for entity in describable_entities:
            area_comp = entity.get_comp("Area")
            if area_comp and entity.id != players_current_position.at_entity_id:
                continue

            if random.random() > self.description_chance:
                continue

            context_tags = self.context_builder.build(entity, world_state)

            description = self.get_random_description(
                entity.name,
                "ambient",
                context_tags
            )

            if description is None:
                description = self.get_random_description(
                    entity.id,
                    "ambient",
                    context_tags
                )

            if description is None:
                continue

            chronicles.append(
                f"{entity.name}:\n - {description}"
            )
            break

    def can_describe(self, entity):
        return entity.has_comp("Area")

    def get_random_description(
        self,
        entity_key,
        description_type,
        context_tags
    ):

        valid_descriptions = self.find_valid_descriptions(
            entity_key,
            description_type,
            context_tags
        )

        if not valid_descriptions:
            return None

        chosen_description = random.choice(valid_descriptions)

        return random.choice(chosen_description["texts"])

    def find_valid_descriptions(
        self,
        entity_key,
        description_type,
        context_tags
    ):

        entity_descriptions = self.descriptions.get(entity_key, {})
        valid_descriptions = []

        for description in entity_descriptions.get(description_type, []):

            required_tags = description.get("required_tags", [])
            forbidden_tags = description.get("forbidden_tags", [])

            if not self.context_builder.tags_match(
                required_tags,
                forbidden_tags,
                context_tags
            ):
                continue

            valid_descriptions.append(description)

        return valid_descriptions
