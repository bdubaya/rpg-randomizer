from objects.randomobject import RandomObject
from objects.door import Door
from objects.npc import Npc
import random

class Room(RandomObject):
    parameter_types = []

    # Describe the doorways as well
    def describe(self,from_perspective=None):
        print(super().describe())
        print("========================")
        self.describe_set(self.npcs,"NPCs")
        self.describe_set(self.doorways,"doors")

    def describe_set(self, set_type, descriptor):
        if len(set_type) == 0:
            return
        print("There are {0} {1} here.".format(len(set_type), descriptor))
        incr = 0
        for set_item in set_type:
            incr += 1
            print("{0}:  {1}".format(incr, set_item.describe(self)))
        print("------------------------")

    # Add a door to the doorways list if it is unique
    def add_door(self,doorway):
        if doorway not in self.doorways:
            self.doorways.append(doorway)

    # Get a door from the doorways list if it exists, otherwise return null
    def get_door(self,num):
        try:
            return self.doorways[num]
        except IndexError:
            return None

    # Try to open a specific door from this room
    def open_door(self,door):
        if door.open(self) is None:
            door.connect(self,Room())
        return door.open(self)

    # Also add a random number of doors
    def __init__(self):
        super().__init__()
        self.doorways = []
        for door_num in range(0, random.randint(1,3)):
            self.add_door(Door(self))
        self.createNpcs()

    def createNpcs(self):
        self.npcs = []
        number_npcs = RandomObject.sqrt_random(0,4,1000)
        for x in range(0,number_npcs):
            self.npcs.append(Npc())
