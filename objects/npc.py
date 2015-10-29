from objects.randomobject import RandomObject
from objects.spellbookgenerator import SpellBookGenerator
from random import shuffle
import random

class Npc(RandomObject):
    parameter_types = []

    def __init__(self):
        super().__init__("data/unlocked/character.json")
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        self.level = random.randint(0, 20) + 1
        self.spell_book = ""
        self.sbg = SpellBookGenerator()

    def describe(self,from_perspective=None):
        description = '\n'
        if self.sbg.hasSpells(self.playable_class):
            if self.spell_book is "":
                self.spell_book = self.makeSpellBook()
            description += self.spell_book
        description = super().describe(from_perspective) + description
        return description

    def makeSpellBook(self):
        spell_preferences = ['Abjuration','Conjuration','Divination','Evocation','Illusion','Necromancy','Transmutation']
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
        else:
            typename = 'Transmuter'

        self.playable_class = '{0} ({1})'.format(self.playable_class, typename)
