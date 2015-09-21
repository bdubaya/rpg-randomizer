import random, re, json

class RandomObject:

    def describe(self):
        # Use the description value in the json, then reflect it into a formatter
        desc_raw = getattr(self,'description')['value']
        desc_values = list(getattr(self,x) for x in getattr(self,'description')['keys'])
        print(desc_raw.format(*desc_values))
        print()

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
        reader.parameter_types = {k:v for (k,v) in all_random_parameters[reader_name].items() if not 'description' in k}
        reader.description = all_random_parameters[reader_name]['description']

class Door(RandomObject):
    parameter_types = []

    def connect(self,room_a,room_b):
        self.rooms = [room_a, room_b]

    def describe(self):
        print('nope')

    def open(self,open_from):
        if open_from in self.rooms:
            return list(filter(lambda x: x != open_from, self.rooms))[0]
        return open_from

    def __init__(self, room_a,room_b=None):
        room_a.add_door(self)
        if room_b is not None:
            room_b.add_door(self)
        self.connect(room_a,room_b)
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)


class Room(RandomObject):
    parameter_types = []

    def describe(self):
        super().describe()
        if len(self.doorways) > 0:
            print("There are {0} doors here, described as follows...".format(len(self.doorways)))
            for door in self.doorways:
                print("Door #{0}".format(self.doorways.index(door) + 1))
                door.describe()

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
        self.doorways = []
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)
        for door_num in range(0, random.randint(1,4)):
            self.add_door(Door(self))



# Dungeon class has the layout of all rooms
class Dungeon(RandomObject):
    parameter_types = []

    def connect(self, new_room, existing_room):
        # Only adds along x-axis at the moment...
        doorway = Door(new_room,existing_room)
        dimensions = [int(x / 5) for x in existing_room.dimensions()]

    def __init__(self):
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)



# Let's do some testing
donj = Dungeon()
first_room = Room()

print("description of the dungeon")
donj.describe()

current_room = first_room
while True:
    print('The room you are in now is...')
    current_room.describe()
    door_num = input("Which door would you like to take?")

    door = current_room.get_door(int(door_num) -1)
    if door is not None:
        current_room = current_room.open_door(door)
