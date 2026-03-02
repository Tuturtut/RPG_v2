from components.base import Position

class PrisonDirector:
    def __init__(self, entity_factory):
        self.factory = entity_factory


    def update(self, entities, world_state):
        spawn_area_id = None

        for eid, e in entities.items():
            if e.get_comp("Area") and e.has_tag("bread_spawn_location"):
                spawn_area_id = eid
                break

        if not spawn_area_id:
            return
        
        clock = world_state["engine"].get_comp("GameClock")


        if clock.tick % 50 == 0:
            bread = self.factory.create_item("Miche de pain", "FOOD")
            bread.add_comp(Position(at_entity_id=spawn_area_id))
            world_state["world"].entities[bread.id] = bread

            world_state["chronicles"].append("Une miche de pain tombe lourdement sur le sol froid.")