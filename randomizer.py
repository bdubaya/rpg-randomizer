import random, json, math

class RandomObject:

    def describe(self):
        # Use the description value in the json, then reflect it into a formatter
        desc_raw = getattr(self,'description')
        desc_values = list(getattr(self,x) for x in getattr(self,'description_keys'))
        # This line mutates the string with a description_mutator
        pre_mutation = desc_raw.format(*desc_values)
        return pre_mutation.format(*desc_values)

    def randomize(self, type_to_randomize):
        type_value = self.parameter_types[type_to_randomize]
        # Get a random number between 0 and (len-1). This fixes an Ob1 error
        random_val = random.randint(0,len(type_value)-1)
        result = type_value[random_val]
        # Use reflection to set the type attribute to the result
        setattr(self,type_to_randomize,result)

    def read_in_random_parameters(reader):
        reader_name = reader.__class__.__name__.lower()
        all_random_parameters = json.load(open("RandomValues.txt",'r'))
        reader.parameter_types = {k:v for (k,v) in all_random_parameters[reader_name].items() if not 'description_keys' in k}
        reader.description_keys = all_random_parameters[reader_name]['description_keys']

    def __init__(self):
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)

class Direction(RandomObject):
    parameter_types = []

    def opposite(self):
        origins = self.parameter_types['origin']
        index = origins.index(self.origin)
        category = math.floor(index / 2)
        return origins[((index - 2*category + 1) % 2) + 2*category]

class Door(RandomObject):
    parameter_types = []

    def describe(self,from_room):
        self.location = self.locations[from_room]
        return super().describe()

    def connect(self,room_a,room_b):
        if room_a is not None:
            room_a.add_door(self)
        if room_b is not None:
    	    room_b.add_door(self)
        self.rooms = [room_a, room_b]
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

    def describe(self):
        print(super().describe())
        if len(self.doorways) is 0:
            return
        print("There are {0} doors here.".format(len(self.doorways)))
        incr = 0
        for door in self.doorways:
            incr += 1
            print("{0}:  {1}".format(incr, door.describe(self)))

    def add_door(self,doorway):
        if doorway not in self.doorways:
            self.doorways.append(doorway)

    def get_door(self,num):
        try:
            return self.doorways[num]
        except IndexError:
            return None

    def open_door(self,door):
        if door.open(self) is None:
            door.connect(self,Room())
        return door.open(self)

    def dimensions(self):
        dim = re.split('(\d*)x(\d*)', self.dimension)
        return (int(dim[1]), int(dim[2]))

    def __init__(self):
        super().__init__()
        self.doorways = []
        for door_num in range(0, random.randint(1,3)):
            self.add_door(Door(self))

# Dungeon is a blank object used for flavor at the moment.
class Dungeon(RandomObject):
    parameter_types = []

    def describe(self):
        print(super().describe())



# Let's do some testing
donj = Dungeon()
first_room = Room()

donj.describe()
current_room = first_room
while True:
    print()
    current_room.describe()
    door_num = input("\nWhich door would you like to take?  ")

    door = current_room.get_door(int(door_num) -1)
    if door is not None:
        current_room = current_room.open_door(door)
