from objects.Npc import Npc
import sys

class NpcRandomizer(object):
    def __init__(self, desired_class=''):
        self.desired_class = desired_class

    def get(self, num):
        return [Npc(self.desired_class) for i in range(0,num)]

desired_class = ''
number_to_generate = 1

for x in range(1,len(sys.argv)):
    try:
        number_to_generate = int(sys.argv[x])
    except:
        desired_class = sys.argv[x]

# Create and describe a certain number
gen = NpcRandomizer(desired_class)
for npc in gen.get(number_to_generate):
    print(npc.describe())
