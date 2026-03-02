from rich import print
from rich.panel import Panel
from rich.text import Text

class RenderSystem:
    def __init__(self, mode="FULL"):
        self.mode = mode

    def update(self, entities, world_state):
        print(f"\n[bold white]─── TOUR {world_state.get('tick', 0)} ───[/bold white]")

        # 1. RÉCUPÉRATION DES DONNÉES
        areas = [e for e in entities if entities[e].get_comp("Area")]
        actors = [e for e in entities if not entities[e].get_comp("Area") and not entities[e].get_comp("Trade_Request") and entities[e].has_comp("Health")]
        items = [e for e in entities if entities[e].get_comp("Item")]
        logs = world_state.get("chronicles", []) # On récupère les phrases du Traducteur

        # 2. AFFICHAGE DU JOURNAL (Si mode LOG_ONLY ou FULL)
        if self.mode in ["LOG_ONLY", "FULL"]:
            if logs:
                print("[italic yellow]📜 Chroniques de la Fosse :[/italic yellow]")
                # On n'affiche que les 5 derniers messages pour ne pas polluer
                for log in logs[-5:]:
                    print(f"  [antiquewhite1]“{log}”[/antiquewhite1]")
                print("")

        if self.mode == "LOG_ONLY":
            return # On s'arrête là

        # 3. AFFICHAGE DES LIEUX (Si mode MAP ou FULL)
        if self.mode in ["MAP", "FULL"]:
            for a in areas:
                area = entities[a]
                print(f"[blue]{area.name.upper()}[/blue]")

        # 4. AFFICHAGE DES ACTEURS (Sauf si mode MAP)
        if self.mode in ["ACTORS_ONLY", "FULL"]:
            for e in actors:
                actor = entities[e]
                self.render_entity(actor)
        
        if self.mode in ["ITEMS_ONLY", "FULL"]:
            for e in items:
                item = entities[e]
                self.render_entity(item)

    def render_entity(self, e):
        dead = e.get_comp("Dead")
        pos = e.get_comp("Position")
        
        # Cas : Entité morte
        if dead:
            loc = f" @{pos.location_name}" if pos else ""
            print(f"[bright_black]▶ {e.name.upper()} {loc} (Décédé)[/bright_black]")
            return

        # Construction de l'en-tête (Nom + Position + Action)
        header = self._build_header(e)
        print(header)

        # Construction des détails (Stats + Inventaire)
        details = self._build_details(e)
        if details:
            print(details)

    def _build_header(self, e):
        pos = e.get_comp("Position")
        mov = e.get_comp("Movement")
        act = e.get_comp("ActionRequest")

        #action request
        
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
        mood = e.get_comp("Mood")
        inv = e.get_comp("Inventory")
        health = e.get_comp("Health")
        hunger = e.get_comp("Hunger")
        mindset = e.get_comp("Mindset") # On anticipe tes nouveaux composants !

        lines = []

        # Ligne 1 : Stats vitales (côte à côte)
        stats = []
        if health: stats.append(f"HP {self._color_stat(health.current_health, health.max_health)}")
        if hunger: stats.append(f"Faim {self._color_stat(hunger.current, hunger.max_val)}")
        if stats: lines.append(f"  └─ {' | '.join(stats)}")

        # Ligne 2 : État d'esprit et Feeling
        state_line = ""
        if mindset: state_line += f"[italic]{mindset.trait}[/italic] "
        if mood: state_line += f"• [bold]{mood.feeling}[/bold]"
        if state_line: lines.append(f"  └─ {state_line}")

        # Ligne 3 : Inventaire
        if inv and inv.items:
            items_str = " ".join([f"[white][{i.name}][/white]" for i in inv.items])
            lines.append(f"  └─ inv {items_str}")

        return "\n".join(lines) if lines else None

    def _color_stat(self, current, max_val):
        """Colorise la stat selon son niveau (Vert -> Jaune -> Rouge)"""
        ratio = current / max_val if max_val > 0 else 0
        color = "green"
        if ratio < 0.3: color = "red"
        elif ratio < 0.6: color = "yellow"
        return f"[{color}]{current}/{max_val}[/{color}]"