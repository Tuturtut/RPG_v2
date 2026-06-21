from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RichLog
from textual.containers import Container

from textualRender import TextualRender

from entity import Entity
from world import World

from components.base import Area, Position, GameClock, Movement, Schedule, ScheduledAction, ScheduledActivity
from components.biology import Health, Hunger
from components.economy import Inventory    

from systems.healthSystem import HealthSystem
from systems.hungerSystem import HungerSystem
from systems.eatingSystem import EatingSystem
from systems.deleteSystem import DeleteSystem
from systems.timeSystem import TimeSystem
from systems.talkingSystem import TalkingSystem
from systems.descriptionSystem import DescriptionSystem
from systems.movementSystem import MovementSystem
from systems.goalResolutionSystem import GoalResolutionSystem
from systems.scheduleSystem import ScheduleSystem



class App(App):
    BINDINGS = [("space", "next_turn", "Jour suivant"), ("q", "quit", "Quitter")]
    CSS = """
        #main_area {
            layout: grid;
            grid-size: 2;
            grid-columns: 2fr 3fr;
        }
        #pnj_view, #logs{
            border-left: solid gray;
            height: 100%;
            padding: 1;
            color: #FFFFFF;
            background: #111111;
        }
        """
    
    DARK = True

    def on_mount(self, event):

        self.world = World()

        self.renderer = TextualRender(self.world.world_state, mode="FULL")

        world_engine_id = self.world.create_entity(id="world_engine", name="Moteur du monde")
        self.world.add_comp(world_engine_id, GameClock())

        self.world.world_state["engine"] = self.world.entities[world_engine_id]


        tavern_id = self.world.create_entity(id="tavern", name="Taverne")
        self.world.add_comp(tavern_id, Area())
        self.world.add_tag(tavern_id, "tavern")

        forest_id = self.world.create_entity(id="forest", name="Forêt")
        self.world.add_comp(forest_id, Area())
        self.world.add_tag(forest_id, "forest")


        infiltrator_id = self.world.create_entity(id="infiltrator", name="Infiltrator")
        self.world.add_comp(infiltrator_id, Position(tavern_id))
        self.world.add_comp(infiltrator_id, Health())
        self.world.add_tag(infiltrator_id, "player")

        tavern_keeper_id = self.world.create_entity(id="tavern_keeper", name="Tavern Keeper")
        self.world.add_comp(tavern_keeper_id, Position(tavern_id))
        self.world.add_comp(tavern_keeper_id, Health())
        self.world.add_tag(tavern_keeper_id, "innkeeper")
        self.world.add_comp(tavern_keeper_id, Schedule(items=[
            ScheduledAction(hour=8, action="open_tavern"),
            ScheduledAction(hour=22, action="close_tavern"),
            ScheduledActivity(start=8, end=22, activity="manage_tavern")
        ]))

        knight_id = self.world.create_entity(id="knight", name="Knight")
        self.world.add_comp(knight_id, Position(forest_id))
        self.world.add_comp(knight_id, Health())
        self.world.add_comp(knight_id, Schedule(items=[
            ScheduledAction(hour=8, action="walk_in_forest"),
            ScheduledAction(hour=12, action="eat"),
            ScheduledAction(hour=16, action="walk_in_forest"),
            ScheduledAction(hour=20, action="rest"),
        ]))

        squire_id = self.world.create_entity(id="squire", name="Squire")
        self.world.add_comp(squire_id, Position(tavern_id))
        self.world.add_comp(squire_id, Health())
        self.world.add_tag(squire_id, "young")
        self.world.add_comp(squire_id, Schedule(items=[
            ScheduledActivity(start=8, end=12, activity="train"),
            ScheduledAction(hour=12, action="eat"),
            ScheduledActivity(start=13, end=17, activity="train"),
        ]))


        self.world.world_state["player"] = self.world.entities[infiltrator_id]
        self.world.add_system(ScheduleSystem())
        self.world.add_system(GoalResolutionSystem())
        self.world.add_system(MovementSystem())
        self.world.add_system(DescriptionSystem())
        self.world.add_system(TalkingSystem())
        self.world.add_system(TimeSystem())
        self.world.add_system(DeleteSystem())



    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main_area"):
            yield Static("PNJ", id="pnj_view")
            yield RichLog(id="logs")
        yield Footer()

    def take_other_area(self, current_area_id, areas):
        other_areas = [area_id for area_id in areas if area_id != current_area_id]
        return other_areas[0] if other_areas else None

    
    def action_next_turn(self):
        # 1. On fait tourner la simulation
        self.world.update()

        # 2. On met à jour la vue des PNJ (Colone de gauche)
        pnj_view = self.query_one("#pnj_view", Static)
        pnj_view.update(self.renderer.get_pnj_view(self.world.entities))

        # 3. On met à jour les Logs (Colone de droite)
        log_view = self.query_one("#logs", RichLog)
        
        # On vide les chroniques vers le log_view
        if "chronicles" in self.world.world_state:
            for log in self.world.world_state["chronicles"]:
                log_view.write(f"{log}")
            self.world.world_state["chronicles"] = [] # On vide après affichage
        
        if "logs" in self.world.world_state:
            for log in self.world.world_state["logs"]:
                log_view.write(f"{log}")
            self.world.world_state["logs"] = []

if __name__ == "__main__":
    app = App()
    app.run()
