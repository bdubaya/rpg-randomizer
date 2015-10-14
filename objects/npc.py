from objects.randomobject import RandomObject

class Npc(RandomObject):
    parameter_types = []

    def __init__(self):
        super().__init__()

    def describe(self,from_perspective=None):
        return super().describe(from_perspective)
