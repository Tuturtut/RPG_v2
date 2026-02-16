from components.economy import TradeRequest
from entity import Entity

from components.base import Position
from components.base import Area
from components.base import ActionRequest

from components.biology import Hunger

from components.social import Mood

from components.economy import Inventory
from components.economy import Service


from systems.aiSystem import AISystem
from systems.deleteSystem import DeleteSystem
from systems.eatingSystem import EatingSystem
from systems.hungerSystem import HungerSystem
from systems.moveSystem import MoveSystem
from systems.tradeSystem import TradeSystem
from systems.renderSystem import RenderSystem

from world import World


# Initialisation du monde
w = World()

auberge = Entity("Auberge")
auberge.add_comp(Inventory(["Biere", "Biere", "Biere"]))
auberge.add_comp(Area())
auberge.add_comp(Service("FOOD"))


# Création de Jean le Forgeron
jean = Entity("Jean le Forgeron")
jean.add_comp(Position("Forge"))
jean.add_comp(Mood())
jean.add_comp(Inventory())
jean.add_comp(Hunger(10, 10))

charles = Entity("Charles")
charles.add_comp(Position("Maison"))
charles.add_comp(Mood("Bien"))
charles.add_comp(Inventory(["Pierre", "Biere"]))
charles.add_comp(Hunger(12, 12))

# # Création d'un Ours (qui n'a pas de routine ni de mood, juste une position)
# ours = Entity("Ours sauvage")
# ours.add_comp(Position("Forêt"))



w.add_entity(jean)
# w.add_entity(ours)
w.add_entity(charles)
w.add_entity(auberge)

# Ajout des systèmes
w.add_system(TradeSystem())
w.add_system(MoveSystem())
w.add_system(HungerSystem())
w.add_system(EatingSystem())
w.add_system(AISystem())

w.add_system(RenderSystem()) # A la toute fin
w.add_system(DeleteSystem())

# --- SIMULATION ---
for i in range(60):
    w.update()

# # 1. Beau temps, Paix
# my_world.update()

# # 2. Il commence à pleuvoir
# my_world.global_state["is_raining"] = True
# my_world.update()

# # 3. La guerre éclate !
# my_world.global_state["war_declared"] = True
# my_world.update()
