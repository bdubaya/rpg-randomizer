import random, json, math
from rnn.NameRnn import NameRnn

# Globally defined variables are bad but this is something I am doing for performance

print('Loading Neural Net Data...')
neuralnet = NameRnn()
npc_names = neuralnet.get(5)
print('Done!\n')

class RandomObject(object):

    # Use the description value in the json, then reflect it into a formatter
    def describe(self, from_perspective=None):
        # Get the raw string and the list of keys for formatting
        desc_raw = getattr(self,'description')
        desc_values = list(getattr(self,x) for x in getattr(self,'description_keys'))
        # This line mutates the string with a description_mutator
        pre_mutation = desc_raw.format(*desc_values)
        return pre_mutation.format(*desc_values)

    # randomize a field in the json and apply it to this RandomObject
    def randomize(self, type_to_randomize):
        type_value = self.parameter_types[type_to_randomize]
        # Get a random number between 0 and (len-1). This fixes an Ob1 error
        random_val = random.randint(0,len(type_value)-1)
        result = type_value[random_val]
        # Use reflection to set the type attribute to the result
        setattr(self,type_to_randomize,result)

    # Read the Json and add the types and keys to the RandomObject appropriately
    def read_in_random_parameters(reader):
        all_random_parameters = json.load(open("RandomValues.txt",'r'))
        reader_name = reader.__class__.__name__.lower()
        reader.parameter_types = {k:v for (k,v) in all_random_parameters[reader_name].items() if not 'description_keys' in k}
        reader.description_keys = all_random_parameters[reader_name]['description_keys']

    def sqrt_random(minimum,maximum,scale):
        absolute_max = round(math.sqrt(scale))
        random_value = round(math.sqrt(random.randint(1,scale)))
        return int(max(random_value - (absolute_max-maximum), minimum))

    def __init__(self):
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)

class Direction(RandomObject):
    parameter_types = []

    # Get the opposite direction of self.origin according to the json
    def opposite(self):
        origins = self.parameter_types['origin']
        index = origins.index(self.origin)
        # Assumes order of opposing directions being adjacent in the json
        category = math.floor(index / 2)
        return origins[((index - 2*category + 1) % 2) + 2*category]

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
            self.npcs.append(Npc(npc_names.pop()))

class Npc(RandomObject):
    parameter_types = []

    def __init__(self, name):
        super().__init__()
        self.name = name

    def describe(self,from_perspective=None):
        return "{0} named {1}".format(super().describe(), self.name)

# Dungeon is a blank object used for flavor at the moment.
class Dungeon(RandomObject):
    parameter_types = []

    def describe(self,from_perspective=None):
        print(super().describe())



# Let's do some testing
donj = Dungeon()
first_room = Room()

donj.describe()
current_room = first_room
while True:
    print("\n========================")
    current_room.describe()
    door_num = input("\nWhich door would you like to take?  ")

    door = current_room.get_door(int(door_num) -1)
    if door is not None:
        current_room = current_room.open_door(door)
