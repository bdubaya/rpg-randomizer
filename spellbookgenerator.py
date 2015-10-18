import json
from random import shuffle

class SpellBookGenerator(object):
    def __init__(self):
        '''
        Load the spell list JSON
        '''
        self.spells = json.load(open('5e-spells/spells.json','r'))

    def get(self, school_preference, levels):
        '''
        Create a random spell list
        '''
        full_spell_list = [[] for na in range(0,len(levels))]
        for school_pref in school_preference:
            for lvl in range(0,len(levels)):
                level = self.filterByLevel(lvl)
                school = self.filterBySchool(school_pref,level)
                shuffled_spell_list = [spell for spell in school]
                shuffle(shuffled_spell_list)
                if shuffled_spell_list is None:
                    continue
                for spell in shuffled_spell_list:
                    if len(full_spell_list[lvl]) < levels[lvl]:
                        full_spell_list[lvl].append(spell)
        return full_spell_list

    def printList(self, school_preference, levels):
        spell_list = self.get(school_preference,levels)
        for i in range(0,len(spell_list)):
            spells_for_level = ', '.join([spell for spell in spell_list[i]])
            print('Level {0}:  {1}'.format(i,spells_for_level))

    def filterByLevel(self, level, spells=None):
        if spells is None:
            spells = self.spells
        spellnames = [spell for spell in spells if spells[spell]['level'] == level]
        return {spell:spells[spell] for spell in spellnames}

    def filterBySchool(self, school, spells=None):
        if spells is None:
            spells = self.spells
        spellnames =  [spell for spell in spells if spells[spell]['school'] == school]
        return {spell:spells[spell] for spell in spellnames}
