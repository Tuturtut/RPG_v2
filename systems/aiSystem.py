from components.base import Movement
from components.economy import TradeRequest

from rich import print

class AISystem:
    """Gère le comportement des PNJ selon la météo et la guerre."""
    def update(self, entities, world_state):
        for eid, e in entities.items():
            if e.get_comp("Dead"): continue


            pos = e.get_comp("Position")
            routine = e.get_comp("Routine")
            mood = e.get_comp("Mood")
            action = e.get_comp("ActionRequest")

            if action and action.type == "EAT_FOOD":
                target_entity = None
                for target in entities:
                    service = target.get_comp("Service")
                    if service and service.type == "FOOD":
                        target_entity = target
                        break

                if target_entity:
                    if pos.at_entity == target_entity:
                        target_inv = target_entity.get_comp("Inventory")

                        for item in target_inv.items:
                            item_type = item.get_comp("Item")
                            if item_type and item_type.type == "food":


                                from entity import Entity
                                ticket = Entity(f"Ticket_{e.name}")

                                ticket.add_comp(TradeRequest(sender=target_entity, receiver=e, item=item))

                                world_state["world"].add_entity(ticket)
                                break

                    elif not e.get_comp("Movement"):
                        e.add_comp(Movement(direction=target_entity))


            if not pos or not routine:
                continue

            # LOGIQUE SYSTÉMIQUE (Météo)
            if world_state["is_raining"]:
                pos.location = routine.shelter_pos
                if mood: mood.feeling = "Agacé"
            else:
                pos.location = routine.work_pos
                if mood: mood.feeling = "Calme"            

            # LOGIQUE NARRATIVE (Impact "GoT")
            # La guerre prend le dessus sur la météo
            if world_state["war_declared"]:
                pos.location = "Caché à la cave"
                if mood: mood.feeling = "Terrifié"