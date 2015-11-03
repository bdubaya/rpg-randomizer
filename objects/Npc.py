from objects.RandomObject import RandomObject
from objects.SpellBookGenerator import SpellBookGenerator
from random import shuffle
import random, math

class Npc(RandomObject):
    parameter_types = []

    def __init__(self, playable_class=''):
        if playable_class != '':
            self.playable_class = playable_class
        super().__init__("data/unlocked/character.json")
        self.randomize_stats()
        self.level = int(random.betavariate(2,5)*19)+1
        self.randomize_hit_points()
        self.spell_book = ""
        self.sbg = SpellBookGenerator()

    def randomize(self, type_to_randomize):
        if type_to_randomize == 'playable_class':
            if not hasattr(self,'playable_class'):
                self.randomize_class()
            self.stat_preferences = self.parameter_types['playable_class'][self.playable_class]['stat_preference']
            self.hitDie = self.parameter_types['playable_class'][self.playable_class]['hitDie']
            return
        super().randomize(type_to_randomize)

    def randomize_hit_points(self):
        self.hp = self.hitDie + self.ability_score(self.constitution)
        for level in range(1,self.level):
            self.hp += random.randint(1,self.hitDie) + self.ability_score(self.constitution)

    def randomize_class(self):
        type_values = [x for x in self.parameter_types['playable_class']]
        random_val = random.randint(0,len(type_values)-1)
        self.playable_class = type_values[random_val]

    # SLOPPY BUT: It works for now
    def randomize_stats(self):
        val = [0,0,0,0,0,0]
        for x in range(0,6):
            val[x] = 8 + int(random.betavariate(2,4)*12)

        scores = sorted(val, reverse=True)
        for x in range(0,6):
            setattr(self,self.stat_preferences[x],scores[x])

        self.stat_block = '\nSTR:\t{0}\tDEX:\t{1}\tCON:\t{2}\nINT:\t{3}\tWIS:\t{4}\tCHA:\t{5}\n'.format(self.strength,self.dexterity,self.constitution,self.intelligence,self.wisdom,self.charisma)

    def ability_score(self, value):
        return math.floor((value - 10) / 2)

    def describe(self,from_perspective=None):
        description = '\n'

        # Add a spell book if the class has spells
        if self.sbg.hasSpells(self.playable_class):
            if self.spell_book is "":
                self.spell_book = self.create_spell_book()
            description += '----------\n' + self.spell_book

        description = super().describe(from_perspective) + description
        return description

    def create_spell_book(self):
        '''Create a randomized spell list based on a class' spells'''

        # Create preferences for spell schools
        spell_preferences = ['Abjuration','Conjuration','Divination','Enchantment','Evocation','Illusion','Necromancy','Transmutation']
        shuffle(spell_preferences)

        # Create the list
        num_spells = [5+random.randint(0,2),4+random.randint(0,3),3+random.randint(0,3),2+random.randint(0,3),1+random.randint(0,3),random.randint(0,3)]
        spell_list = self.sbg.create_list(self.playable_class, spell_preferences, num_spells)

        self.set_school_specialty(spell_preferences[0])
        return spell_list


    def set_school_specialty(self, type):
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
