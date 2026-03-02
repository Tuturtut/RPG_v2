from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RichLog
from textual.containers import Container

from textualRender import TextualRender

from entity import Entity
from world import World

from components.base import Area, Position, GameClock
from components.biology import Health, Hunger
from components.economy import Inventory    

from systems.renderSystem import RenderSystem
from systems.healthSystem import HealthSystem
from systems.hungerSystem import HungerSystem
from systems.eatingSystem import EatingSystem
from systems.deleteSystem import DeleteSystem
from systems.timeSystem import TimeSystem

from systems.prisonDirector import PrisonDirector

from factories.entityFactory import EntityFactory


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

        self.renderer = TextualRender(self.world.world_state, mode="FULL")

        world_engine_id = self.world.create_entity(id="world_engine", name="Moteur du monde")
        self.world.add_comp(world_engine_id, GameClock())

        prison_id = self.world.create_entity(id="prison", name="Prison")
        self.world.add_comp(prison_id, Area())
        self.world.add_tag(prison_id, "bread_spawn_location")

        the_old_one_id = self.world.create_entity(id="the_old_one", name="L'encien")
        self.world.add_comp(the_old_one_id, Position(at_entity_id=prison_id))
        self.world.add_comp(the_old_one_id, Health(current_health=8, max_health=10))
        self.world.add_comp(the_old_one_id, Hunger(current=7, max_val=10))


        the_young_one_id = self.world.create_entity(id="the_young_one", name="Le jeune")
        self.world.add_comp(the_young_one_id, Position(at_entity_id=prison_id))
        self.world.add_comp(the_young_one_id, Health(current_health=10, max_health=10))
        self.world.add_comp(the_young_one_id, Hunger(current=10, max_val=10))

        self.world.world_state["engine"] = self.world.entities[world_engine_id]


        self.world.add_system(TimeSystem())

        self.world.add_system(HealthSystem())
        self.world.add_system(HungerSystem())
        self.world.add_system(EatingSystem())
        self.world.add_system(PrisonDirector(entity_factory=EntityFactory(world_state=self.world.world_state)))

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

        tick = self.world.world_state["engine"].get_comp("GameClock").tick
        
        # On affiche le tour actuel
        log_view.write(f"\n─── TOUR {tick} ───")
        
        # On vide les chroniques vers le log_view
        if "chronicles" in self.world.world_state:
            for log in self.world.world_state["chronicles"]:
                log_view.write(f"“{log}”")
            self.world.world_state["chronicles"] = [] # On vide après affichage
        
        if "logs" in self.world.world_state:
            for log in self.world.world_state["logs"]:
                log_view.write(f"{log}")
            self.world.world_state["logs"] = []

    
if __name__ == "__main__":
    app = App()
    app.run()