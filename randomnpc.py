from objects.npc import Npc

class NpcRandomizer(object):
    def __init__(self):
        pass

    def get(self, num):
        return [Npc() for i in range(0,num)]
