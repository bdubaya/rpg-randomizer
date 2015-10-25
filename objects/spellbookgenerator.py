import json
from random import shuffle

class SpellBookGenerator(object):
    def __init__(self):
        '''
        Load the spell list JSON
        '''
        self.spells = json.load(open('data/unlocked/spells.json','r'))

    def get(self, school_preference, spells_per_level):
        '''
        Create a random spell list
        '''
        full_spell_list = [[] for na in range(0,len(spells_per_level))]
        for school_pref in school_preference:
            for lvl in range(0,len(spells_per_level)):
                level = self.filterByLevel(lvl)
                school = self.filterBySchool(school_pref,level)
                shuffled_spell_list = [spell for spell in school]
                if shuffled_spell_list is None:
                    continue
                shuffle(shuffled_spell_list)
                for spell in shuffled_spell_list:
                    if len(full_spell_list[lvl]) < spells_per_level[lvl]:
                        full_spell_list[lvl].append(spell)
        return full_spell_list

    def createList(self, school_preference, levels):
        spell_list = self.get(school_preference,levels)
        out = ""
        for i in range(0,len(spell_list)):
            spells_for_level = ', '.join([spell for spell in spell_list[i]])
            out += 'Level {0}:  {1}\n'.format(i,spells_for_level)
        return out

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

    def identify(self, spell):
        if (spell is "" and not spell in self.spells):
            return
        print('\n{0}\n=========='.format(spell))
        for key in self.spells[spell]:
            print('{0}: {1}'.format(key,self.spells[spell][key]))
