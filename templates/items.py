from components.economy import Item
from components.economy import Value

from entity import Entity

ITEM_TEMPLATES = {
    "biere" : {"name": "Bière", "comps": [Item(type="food"), Value(value=1)]},
}

def create_from_template(world, template_id):
    data = ITEM_TEMPLATES[template_id]
    e = Entity(data["name"])
    for c in data["comps"]:
        import copy
        e.add_comp(copy.deepcopy(c))
    return e