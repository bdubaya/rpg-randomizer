from objects.npc import Npc
import sys

class NpcRandomizer(object):
    def __init__(self, desired_class=''):
        self.desired_class = desired_class

    def get(self, num):
        return [Npc(self.desired_class) for i in range(0,num)]

desired_class = ''
if len(sys.argv) > 1:
    desired_class = sys.argv[1]

# Gimme 5
gen = NpcRandomizer(desired_class)
for npc in gen.get(5):
    print(npc.describe())
