
import keyboard

from entity import Entity
from world import World

from components.base import Area, Position
from components.biology import Health, Hunger, Mindset
from components.economy import Inventory

from systems.prisonDirector import PrisonDirector
from systems.renderSystem import RenderSystem
from systems.healthSystem import HealthSystem
from systems.hungerSystem import HungerSystem
from systems.eatingSystem import EatingSystem
from systems.deleteSystem import DeleteSystem

from factories.entityFactory import EntityFactory

from rich import print

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

w = World()
w.add_entity(prison)
w.add_entity(the_old_one)
w.add_entity(the_young_one)


w.add_system(HealthSystem())
w.add_system(HungerSystem())
w.add_system(EatingSystem())

w.add_system(DeleteSystem())

w.add_system(RenderSystem(mode="FULL"))


def wait_for_key():
    print("[italic][bright_black]Appuyez sur une touche pour continuer...[/bright_black][/italic]")
    keyboard.wait("space")


game_running = True
while game_running:
    w.update()
    wait_for_key()