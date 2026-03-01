from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RichLog
from textual.containers import Container

from factories.entityFactory import EntityFactory
from systems.prisonDirector import PrisonDirector
from textualRender import TextualRender

from entity import Entity
from world import World

from components.base import Area, Position
from components.biology import Health, Hunger
from components.economy import Inventory    

from systems.renderSystem import RenderSystem
from systems.healthSystem import HealthSystem
from systems.hungerSystem import HungerSystem
from systems.eatingSystem import EatingSystem
from systems.deleteSystem import DeleteSystem

class App(App):
    BINDINGS = [("space", "next_turn", "Jour suivant"), ("q", "quit", "Quitter")]
    CSS = """
        #main_area {
            layout: grid;
            grid-size: 2;
        }
        #pnj_view, #logs{
            border: solid green;
            height: 100%;
            padding: 1;
            color: #FFFFFF;
            background: #1e1e1e;
        }"""
    
    DARK = True

    def on_mount(self, event):

        self.world = World()

        self.renderer = TextualRender(mode="FULL")

        prison = Entity("Prison")
        prison.add_comp(Area())
        prison.add_tag("bread_spawn_location")

        the_old_one = Entity("L'encien")
        the_old_one.add_comp(Position(location_name="Prison", at_entity=prison))
        the_old_one.add_comp(Health(current_health=8, max_health=10))
        the_old_one.add_comp(Hunger(current=7, max_val=10))
        # the_old_one.add_comp(Inventory())
        # the_old_one.add_comp(Mindset(trait="stoic"))

        the_young_one = Entity("Le jeune")
        the_young_one.add_comp(Position(location_name="Prison", at_entity=prison))
        the_young_one.add_comp(Health(current_health=10, max_health=10))
        the_young_one.add_comp(Hunger(current=10, max_val=10))
        # the_young_one.add_comp(Inventory())
        # the_young_one.add_comp(Mindset(trait="unstable"))

        self.world.add_entity(prison)
        self.world.add_entity(the_old_one)
        self.world.add_entity(the_young_one)

        self.world.add_system(HealthSystem())
        self.world.add_system(HungerSystem())
        self.world.add_system(EatingSystem())
        self.world.add_system(PrisonDirector(entity_factory=EntityFactory(world_state=self.world.global_state)))

        self.world.add_system(DeleteSystem())



    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main_area"):
            yield Static("PNJ", id="pnj_view")
            yield RichLog(id="logs")
        yield Footer()
    
    def action_next_turn(self):
        # 1. On fait tourner la simulation
        self.world.update()

        # 2. On met à jour la vue des PNJ (Colone de gauche)
        pnj_view = self.query_one("#pnj_view", Static)
        pnj_view.update(self.renderer.get_pnj_view(self.world.entities))

        # 3. On met à jour les Logs (Colone de droite)
        log_view = self.query_one("#logs", RichLog)
        
        # On affiche le tour actuel
        log_view.write(f"\n─── TOUR {self.world.global_state.get('tick')} ───")
        
        # On vide les chroniques vers le log_view
        if "chronicles" in self.world.global_state:
            for log in self.world.global_state["chronicles"]:
                log_view.write(f"“{log}”")
            self.world.global_state["chronicles"] = [] # On vide après affichage
        
        if "logs" in self.world.global_state:
            for log in self.world.global_state["logs"]:
                log_view.write(f"“{log}”")
            self.world.global_state["logs"] = []

    
if __name__ == "__main__":
    app = App()
    app.run()