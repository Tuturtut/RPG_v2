from rich.text import Text
from rich.console import Console

class TextualRender:
    def __init__(self, mode="FULL"):
        self.mode = mode

    def get_pnj_view(self, entities):
        """Retourne la string formatée pour le widget pnj_view."""
        output = []
        
        # 1. RÉCUPÉRATION DES LIEUX ET ACTEURS
        areas = [e for e in entities if e.get_comp("Area")]
        actors = [e for e in entities if not e.get_comp("Area") and e.has_comp("Health")]
        items = [e for e in entities if e.get_comp("Item")]

        # 2. LIEUX
        for a in areas:
            output.append(f"[blue b]{a.name.upper()}[/blue b]")

        # 3. ACTEURS
        for e in actors:
            output.append(self.render_entity(e))
        
        # 4. OBJETS AU SOL
        if items:
            output.append("\n[italic white]Objets au sol :[/]")
            for i in items:
                output.append(f" [yellow]○[/] {i.name}")

        return "\n".join(output)

    def render_entity(self, e):
        """Identique à ton ancien code, mais retourne la string."""
        dead = e.get_comp("Dead")
        pos = e.get_comp("Position")
        
        if dead:
            loc = f" @{pos.location_name}" if pos else ""
            return f"[bright_black]▶ {e.name.upper()} {loc} (Décédé)[/bright_black]"

        header = self._build_header(e)
        details = self._build_details(e)
        
        if details:
            return f"{header}\n{details}\n"
        return f"{header}\n"

    def _build_header(self, e):
        pos = e.get_comp("Position")
        mov = e.get_comp("Movement")
        act = e.get_comp("ActionRequest")
        
        name_part = f"[green]▶ {e.name.upper()}[/green]"
        pos_part = ""
        if pos:
            if mov:
                pos_part = f" [blue]@{pos.location_name} ➔ {mov.direction.name}[/blue]"
            else:
                pos_part = f" [blue]@{pos.location_name}[/blue]"

        act_part = f" [yellow][{act.type.lower()}][/yellow]" if act else ""
        return f"{name_part}{pos_part}{act_part}"

    def _build_details(self, e):
        # ... Garde exactement ton code actuel pour _build_details et _color_stat ...
        # Copie-colle tes méthodes ici, elles fonctionnent parfaitement avec Textual !
        mood = e.get_comp("Mood")
        inv = e.get_comp("Inventory")
        health = e.get_comp("Health")
        hunger = e.get_comp("Hunger")
        mindset = e.get_comp("Mindset")

        lines = []
        stats = []
        if health: stats.append(f"HP {self._color_stat(health.current_health, health.max_health)}")
        if hunger: stats.append(f"Faim {self._color_stat(hunger.current, hunger.max_val)}")
        if stats: lines.append(f"  └─ {' | '.join(stats)}")

        state_line = ""
        if mindset: state_line += f"[italic]{mindset.trait}[/italic] "
        if mood: state_line += f"• [bold]{mood.feeling}[/bold]"
        if state_line: lines.append(f"  └─ {state_line}")

        if inv and inv.items:
            items_str = " ".join([f"[white][{i.name}][/white]" for i in inv.items])
            lines.append(f"  └─ inv {items_str}")

        return "\n".join(lines) if lines else None

    def _color_stat(self, current, max_val):
        ratio = current / max_val if max_val > 0 else 0
        color = "green"
        if ratio < 0.3: color = "red"
        elif ratio < 0.6: color = "yellow"
        return f"[{color}]{current}/{max_val}[/{color}]"