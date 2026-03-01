from components.base import Position

class PrisonDirector:
    def __init__(self, entity_factory):
        self.factory = entity_factory


    def update(self, entities, world_state):
        entity_location = None

        for e in world_state["world"].entities:
            if e.get_comp("Area") and e.has_tag("bread_spawn_location"):
                entity_location = e
        
        clock = world_state["engine"].get_comp("GameClock")


        if clock.tick % 50 == 0:
            bread = self.factory.create_item("Miche de pain", "FOOD")
            bread.add_comp(Position(location_name="Prison", at_entity=entity_location))
            world_state["world"].entities.append(bread)

            world_state["chronicles"].append("Une miche de pain tombe lourdement sur le sol froid.")