from objects.RandomObject import RandomObject
from objects.Direction import Direction
#from objects import Room, RandomObject, Direction

class Door(RandomObject):
    parameter_types = []

    # Set our location for the description using from_room and the dict
    def describe(self,from_perspective):
        self.location = self.locations[from_perspective]
        return super().describe()

    def connect(self,room_a,room_b):
        # Add this doorway to rooms which are not null
        if room_a is not None:
            room_a.add_door(self)
        if room_b is not None:
    	    room_b.add_door(self)
        self.rooms = [room_a, room_b]
        # Dictionary shows which room is in which direction of the door
        self.locations = {room_a: self.locator.origin, room_b: self.locator.opposite()}

    def open(self,open_from):
        # check to see if this room is in the pair
        if open_from in self.rooms:
            # return it if it exists
            return list(filter(lambda x: x != open_from, self.rooms))[0]
        # otherwise return the current room
        return open_from

    def __init__(self, room_a,room_b=None):
        self.locator = Direction()
        self.connect(room_a,room_b)
        super().__init__()
