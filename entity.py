class Entity:
    def __init__(self, name):
        self.name = name
        self.components = {}
    
    def get_name(self):
        return f"[green]{self.name.upper()}[/green]"

    def add_comp(self, component):
        self.components[type(component).__name__] = component
        return self

    def get_comp(self, component_name):
        return self.components.get(component_name)

    def remove_comp(self, component_name):
        del self.components[component_name]