from objects.randomobject import RandomObject
from objects.spellbookgenerator import SpellBookGenerator
from random import shuffle
import random, math

class Npc(RandomObject):
    parameter_types = []

    def __init__(self, playable_class=''):
        if playable_class != '':
            self.playable_class = playable_class
        super().__init__("data/unlocked/character.json")
        self.randomizeStats()
        self.level = int(random.betavariate(2,5)*19)+1
        self.randomizeHP()
        self.spell_book = ""
        self.sbg = SpellBookGenerator()

    def randomize(self, type_to_randomize):
        if type_to_randomize == 'playable_class':
            if not hasattr(self,'playable_class'):
                self.randomizeClass()
            self.stat_preferences = self.parameter_types['playable_class'][self.playable_class]['stat_preference']
            self.hitDie = self.parameter_types['playable_class'][self.playable_class]['hitDie']
            return
        super().randomize(type_to_randomize)

    def randomizeHP(self):
        self.hp = self.hitDie + self.abilityScore(self.constitution)
        for level in range(1,self.level):
            self.hp += random.randint(1,self.hitDie) + self.abilityScore(self.constitution)

    def randomizeClass(self):
        type_values = [x for x in self.parameter_types['playable_class']]
        random_val = random.randint(0,len(type_values)-1)
        self.playable_class = type_values[random_val]

    # SLOPPY BUT: It works for now
    def randomizeStats(self):
        val = [0,0,0,0,0,0]
        for x in range(0,6):
            val[x] = 8 + int(random.betavariate(2,4)*12)

        scores = sorted(val, reverse=True)
        for x in range(0,6):
            setattr(self,self.stat_preferences[x],scores[x])

        self.stat_block = '\nSTR:\t{0}\tDEX:\t{1}\tCON:\t{2}\nINT:\t{3}\tWIS:\t{4}\tCHA:\t{5}\n'.format(self.strength,self.dexterity,self.constitution,self.intelligence,self.wisdom,self.charisma)

    def abilityScore(self, value):
        return math.floor((value - 10) / 2)

    def describe(self,from_perspective=None):
        description = '\n'
        if self.sbg.hasSpells(self.playable_class):
            if self.spell_book is "":
                self.spell_book = self.makeSpellBook()
            description += '----------\n' + self.spell_book
        description = super().describe(from_perspective) + description
        return description

    def makeSpellBook(self):
        spell_preferences = ['Abjuration','Conjuration','Divination','Enchantment','Evocation','Illusion','Necromancy','Transmutation']
        shuffle(spell_preferences)
        num_spells = [5+random.randint(0,2),4+random.randint(0,3),3+random.randint(0,3),2+random.randint(0,3),1+random.randint(0,3),random.randint(0,3)]
        spell_list = self.sbg.createList(self.playable_class, spell_preferences, num_spells)
        if self.playable_class == 'Wizard':
            self.setMagicSpecialty(spell_preferences[0])
        return spell_list

    def setMagicSpecialty(self, type):
        typename = ''
        if type == 'Abjuration':
            typename = 'Abjurer'
        elif type == 'Conjuration':
            typename = 'Conjurer'
        elif type == 'Divination':
            typename = 'Diviner'
        elif type == 'Evocation':
            typename = 'Evoker'
        elif type == 'Illusion':
            typename = 'Illusionist'
        elif type == 'Necromancy':
            typename = 'Necromancer'
        elif type == 'Enchantment':
            typename = 'Enchanter'
        else:
            typename = 'Transmuter'

        self.playable_class = '{0} ({1})'.format(self.playable_class, typename)
