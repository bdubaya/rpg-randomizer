from objects.Room import Room
from objects.Dungeon import Dungeon

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
