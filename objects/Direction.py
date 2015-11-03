from objects.RandomObject import RandomObject
import math

class Direction(RandomObject):
    parameter_types = []

    # Get the opposite direction of self.origin according to the json
    def opposite(self):
        origins = self.parameter_types['origin']
        index = origins.index(self.origin)
        # Assumes order of opposing directions being adjacent in the json
        category = math.floor(index / 2)
        return origins[((index - 2*category + 1) % 2) + 2*category]
