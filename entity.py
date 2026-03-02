class Entity:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.components = {}
        self.tags = set()
    
    def get_comp(self, component_name):
        return self.components.get(component_name)
    
    def has_comp(self, component_name):
        return component_name in self.components

    def add_comp(self, component):
        self.components[type(component).__name__] = component
        return self
    
    def remove_comp(self, component_name):
        del self.components[component_name]

    def has_tag(self, tag_name):
        return tag_name in self.tags
    