import random
import re

class Room:
  parameter_types = []

  def randomize(self, type_to_randomize):
    shapes = list(filter(lambda x: type_to_randomize + ": " in x, self.random_parameters))
    random_val = random.randint(0,len(shapes)-1)
    setattr(self,type_to_randomize,shapes[random_val])

  def describe(self):
    for params in self.parameter_types:
      print(getattr(self,params))

  def __init__(self, description=None):
    self.random_parameters = open("RandomValues.txt","r").read().split("\n")
    for param in self.random_parameters:
      param_name = param.split(':')[0]
      if param_name not in self.parameter_types:
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

  def add(self, new_room):
    # Use Regex to find the dimensions of the room
    m = re.split('(\d*)x(\d*)', new_room.shape)
    print("Dimensions for room are {0} and {1}".format(m[1], m[2]))




# Let's do some testing
donj = Dungeon()
random_room = donj.at(0,0)
donj.add(Room())
random_room.describe()
