import random, re

class Room:
    parameter_types = []

    def randomize(self, type_to_randomize):
        shapes = list(filter(lambda x: type_to_randomize + ": " in x, self.random_parameters))
        random_val = random.randint(0,len(shapes)-1)
        result = shapes[random_val].split(':')[1]
        setattr(self,type_to_randomize,result)

    def describe(self):
        for params in self.parameter_types:
            print(getattr(self,params))

    def dimensions(self):
        dim = re.split('(\d*)x(\d*)', self.shape)
        return (int(dim[1]), int(dim[2]))


    def __init__(self, description=None):
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
    layout = {frozenset([0,0]) :Room()}

    def at(self, x, y):
        return self.layout[frozenset([x,y])]

    def add(self, new_room, at_x,at_y):
        # Use Regex to find the dimensions of the room
        dimensions = new_room.dimensions()# [dim / 5 for dim in new_room.dimensions()]
        for x in range(0,dimensions[0]):
            for y in range(0,dimensions[1]):
                self.layout.update({frozenset([x,y]):new_room})




# Let's do some testing
donj = Dungeon()
donj.add(Room(),0,0)
random_room = donj.at(0,0)
random_room.describe()
random_room = donj.at(1,1)
random_room.describe()
