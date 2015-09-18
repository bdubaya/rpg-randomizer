import random, re, collections

class Room:
    parameter_types = []
    doorways = []

    def randomize(self, type_to_randomize):
        # Get entries in our RandomValues.txt document which match this type
        type_entries = list(filter(lambda x: type_to_randomize + ": " in x, self.random_parameters))
        # Get a random number between 0 and (len-1). This fixes an Ob1 error
        random_val = random.randint(0,len(type_entries)-1)
        # Take the element at the 1st index, which is the actual value (not key)
        result = type_entries[random_val].split(':')[1]
        # Use reflection to set the type attribute to the result
        setattr(self,type_to_randomize,result)

    def describe(self):
        for params in self.parameter_types:
            print(getattr(self,params))

    def add_door(self,doorway):
        self.doorways.append(doorway)

    def dimensions(self):
        dim = re.split('(\d*)x(\d*)', self.shape)
        return (int(dim[1]), int(dim[2]))


    def __init__(self):
        self.random_parameters = open("RandomValues.txt","r").read().split("\n")
        for param in self.random_parameters:
            param_name = param.split(':')[0]
            if param_name not in self.parameter_types and param_name is not "":
                self.parameter_types.append(param_name)

        for params in self.parameter_types:
            self.randomize(params)


class Door:
    def connect(self,room_a,room_b):
        self.rooms = [room_a, room_b]

    def open(self,open_from):
        if open_from in self.rooms:
            return list(filter(lambda x: x != open_from, self.rooms))[0]
        return None



# Dungeon class has the layout of all rooms
class Dungeon:
    #We use strings for the keys because they are immutable and ordered
    layout = {"" :None}

    def to_key(self,x,y):
        return "{0}x{1}".format(x,y)

    def at(self, x, y):
        try:
            return self.layout[self.to_key(x,y)]
        except KeyError:
            return None

    def add(self, new_room, at_x,at_y):
        # Use Regex to find the dimensions of the room
        dimensions = [int(dim / 5) for dim in new_room.dimensions()]
        # attempt to add the room to the layout map. Overlapping leads may lead to a doorway
        for x in [pre_x + at_x for pre_x in range(0,dimensions[0])]:
            for y in [pre_y + at_y for pre_y in range(0,dimensions[1])]:
                loc = self.to_key(x,y)
                if self.at(x,y) is None:
                    self.layout.update({loc:new_room})






# Let's do some testing
donj = Dungeon()
donj.add(Room(),0,0)
random_room = donj.at(0,0)
dimensions = [int(x / 5) for x in random_room.dimensions()]
donj.add(Room(),dimensions[0],0)

added_room = donj.at(dimensions[0]+1,0)

for x in range(0,dimensions[0]+1):
    print(donj.to_key(x,0))
    donj.at(x,0).describe()
