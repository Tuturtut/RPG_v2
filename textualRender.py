from rich.text import Text
from rich.console import Console

class TextualRender:
    def __init__(self, world_state, mode="FULL"):
        self.mode = mode
        self.world_state = world_state

    def get_pnj_view(self, entities):
        """Retourne la string formatée pour le widget pnj_view."""
        output = []
        
        # 1. RÉCUPÉRATION DES LIEUX ET ACTEURS
        areas = [e for e in entities if entities[e].get_comp("Area")]
        actors = [e for e in entities if not entities[e].get_comp("Area") and entities[e].has_comp("Health")]
        items = [e for e in entities if entities[e].get_comp("Item")]
        engine = self.world_state["engine"]
        if engine.has_comp("GameClock"):
            clock = engine.get_comp("GameClock")
            self.world_state["logs"].append(f"[{clock.str_time}]")

            output.append(f"[bold white]─── JOUR {clock.days} ───[/bold white] [{clock.str_time}]\n")

        # 2. LIEUX
        for area in areas:
            a = entities[area]
            output.append(f"[blue b]{a.name.upper()}[/blue b]")

        # 3. ACTEURS
        for actor in actors:
            a = entities[actor]
            hour = clock.hours if engine.has_comp("GameClock") else None
            output.append(self.render_entity(a, entities, hour=hour))
        
        # 4. OBJETS AU SOL
        if items:
            output.append("\n[italic white]Objets : [/]")
            for item in items:
                i = entities[item]
                pos = i.get_comp("Position")
                loc = ""
                if pos:
                    target_id = pos.at_entity_id
                    area_entity = entities.get(target_id)
                    loc = area_entity.name if area_entity else "Inconnu"
                output.append(f" [goldenrod]○[/] {i.name} [navy]{loc}[/navy]")


        return "\n".join(output)

    def render_entity(self, e, entities, hour=None):
        """Identique à ton ancien code, mais retourne la string."""
        dead = e.get_comp("Dead")
        pos = e.get_comp("Position")
        area_entity = entities.get(pos.at_entity_id)
        
        if dead and area_entity:
            loc = f"@{area_entity.name}" if pos else ""
            return f"[grey]▶ {e.name.upper()} {loc} (Décédé)[/grey]"

        header = self._build_header(e, entities)
        details = self._build_details(e, hour=hour)
        
        if details:
            return f"{header}\n{details}\n"
        return f"{header}\n"

    def _build_header(self, e, entities):
        pos = e.get_comp("Position")
        mov = e.get_comp("Movement")
        act = e.get_comp("ActionRequest")
        
        name_part = f"[orange]▶ {e.name.upper()}[/orange]"
        pos_part = ""
        if pos:
            target_id = pos.at_entity_id
            area_entity = entities.get(target_id)
            area_display_name = area_entity.name if area_entity else "Inconnu"

            if mov:
                pos_part = f" [navy]@{area_display_name} ➔ {mov.direction.name}[/navy]"
            else:
                pos_part = f" [navy]@{area_display_name}[/navy]"

        act_part = f" [yellow][{act.type.lower()}][/yellow]" if act else ""
        return f"{name_part}{pos_part}{act_part}"

    def _build_details(self, e, hour=None):
        # ... Garde exactement ton code actuel pour _build_details et _color_stat ...
        # Copie-colle tes méthodes ici, elles fonctionnent parfaitement avec Textual !
        mood = e.get_comp("Mood")
        inv = e.get_comp("Inventory")
        health = e.get_comp("Health")
        hunger = e.get_comp("Hunger")
        mindset = e.get_comp("Mindset")
        schedule = e.get_comp("Schedule")
        goal = e.get_comp("Goal")

        lines = []
        stats = []
        if health: stats.append(f"HP {self._color_stat(health.current, health.max_val)}")
        if hunger: stats.append(f"Faim {self._color_stat(hunger.current, hunger.max_val)}")
        if stats: lines.append(f"  └─ {' | '.join(stats)}")

        state_line = ""
        if mindset: state_line += f"[italic]{mindset.trait}[/italic] "
        if mood: state_line += f"• [bold]{mood.feeling}[/bold]"
        if state_line: lines.append(f"  └─ {state_line}")

        if inv and inv.items:
            items_str = " ".join([f"[white][{i.name}][/white]" for i in inv.items])
            lines.append(f"  └─ inv {items_str}")

        if schedule and schedule.items and hour is not None:
            current_activity = schedule.get_current_activity(hour)
            if current_activity:
                lines.append(f"  └─ [cyan]Activité :[/cyan] {current_activity}")

        if goal:
            lines.append(f"  └─ [magenta]Objectif :[/magenta] {goal.value}")
        

        return "\n".join(lines) if lines else None

    def _color_stat(self, current, max_val):
        ratio = current / max_val if max_val > 0 else 0
        color = "darkgreen"
        if ratio < 0.3: color = "crimson"
        elif ratio < 0.6: color = "goldenrod"
        return f"[{color}]{current}/{max_val}[/{color}]"
