class Entity:
    def __init__(self, name):
        self.name = name
        self.components = {}
        self.tags = set()
    
    def get_name(self):
        return f"[green]{self.name.upper()}[/green]"

    def add_comp(self, component):
        self.components[type(component).__name__] = component
        return self

    def get_comp(self, component_name):
        return self.components.get(component_name)
    
    def has_comp(self, component_name):
        return component_name in self.components

    def remove_comp(self, component_name):
        del self.components[component_name]
    
    def add_tag(self, tag_name):
        self.tags.add(tag_name)
    
    def has_tag(self, tag_name):
        return tag_name in self.tags
    
    def remove_tag(self, tag_name):
        if tag_name in self.tags:
            self.tags.remove(tag_name)