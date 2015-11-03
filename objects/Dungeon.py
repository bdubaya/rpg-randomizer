from objects.RandomObject import RandomObject

# Dungeon is a blank object used for flavor at the moment.
class Dungeon(RandomObject):
    parameter_types = []

    def describe(self,from_perspective=None):
        print(super().describe())
