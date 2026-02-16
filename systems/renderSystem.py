from rich import print

class RenderSystem:
    """Affiche simplement ce qui se passe dans le terminal."""
    def update(self, entities, world_state):
        print("\n" + "·" * 40)
        print(f"Il {'pleut' if world_state['is_raining'] else 'fait beau'}.")
        if world_state['war_declared']:
            print("Des rumeurs de guerre circulent dans la vallée...")
        print("·" * 40)
        for e in entities:
            if e.get_comp("TradeRequest"): continue

            pos = e.get_comp("Position")
            mood = e.get_comp("Mood")
            inv = e.get_comp("Inventory")
            hunger = e.get_comp("Hunger")
            action = e.get_comp("ActionRequest")
            movement = e.get_comp("Movement")

            line = ""
            line += f"{get_entity_name(e)}"
            if pos:
                if not movement:
                    line += f" [blue]@{pos.location_name}[/blue]"
                else:
                    line += f" [blue]@{pos.location_name} -> {movement.direction.name}[/blue]"
            if action:
                line += f"[bright_black]  --{action.type.lower()}[/bright_black]"
            print(line)

            if mood or inv:
                details = "    └─ "
                if mood: 
                    details += f"{mood.feeling} "
                    details +="\n    └─ "

                if inv:
                    details += "I-("
                    for i in inv.items:
                        details += f"[{i.name}]"
                    details += ")"
                print(details)
            if hunger:
                print(f"    └─ Faim {hunger.current}/{hunger.max_val}")


def get_entity_name(entity):
    area = entity.get_comp("Area")
    if area:
        return f"[blue]{entity.name.upper()}[/blue]"
    else:
        return f"[green]{entity.name.upper()}[/green]"