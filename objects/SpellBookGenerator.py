import json
from random import shuffle
import numpy as np

class SpellBookGenerator(object):
    def __init__(self):
        '''
        Load the spell list JSON
        '''
        self.spells = json.load(open('data/unlocked/spells.json','r'))

    def hasSpells(self,playable_class):
        # When I'm done with the spell list the following line will be removed
        has_classes_specified = [spell for spell in self.spells if 'classes' in self.spells[spell]]
        return len([s for s in has_classes_specified if playable_class in self.spells[s]['classes']]) > 0

    def generate_spellbook(self, playable_class, school_preferences, spells_known_per_level):
        '''
        Create a random spell list based on class, school preferences (e.g. a
        spellcaster who prefers Necromancy, then Evocation, then abjuration,
        etc.), and the number of spells known per spell level
        '''
        full_spell_list = [[] for x in range(0, len(spells_known_per_level))]
        for school_pref in school_preferences:
            for level in range(0, len(spells_known_per_level)):
                spells_at_level = self.get(playable_class, level, school_pref)
                for spell in spells_at_level:
                    if len(full_spell_list[level]) < spells_known_per_level[level]:
                        full_spell_list[level].append(spell)
        return full_spell_list

    def get(self, playable_class, lvl, school):
        '''Filter out all of the spells, then choose those at random'''
        spells_for_class = self.filter_by_class(playable_class)
        spells_for_level = self.filter_by('level', lvl, spells_for_class)
        spells_for_school= self.filter_by('school', school, spells_for_level)
        basic_spells = [spell for spell in spells_for_school]
        shuffle(basic_spells)
        return basic_spells

    def create_list(self, playable_class, school_preferences, levels):
        spell_list = self.generate_spellbook(playable_class, school_preferences,levels)
        out = ""
        for i in range(0,len(spell_list)):
            spells = [spell for spell in spell_list[i]]
            if len(spells) == 0:
                if i > 0:
                    break
                continue
            spells_for_level = ', '.join(sorted(spells))
            out += 'Level {0}:  {1}\n'.format(i,spells_for_level)
        return out

    def filter_by_class(self, playable_class, spells=None):
        if spells is None:
            spells = self.spells

        # When I'm done with the spell list the following line will be removed
        has_classes_specified = [spell for spell in spells if 'classes' in spells[spell]]
        class_spells = [s for s in has_classes_specified if playable_class in spells[s]['classes']]
        return {spell:spells[spell] for spell in class_spells}

    def filter_by(self, filter_type, filter_criterion, spells=None):
        if spells is None:
            spells = self.spells
        spell_names = [s for s in spells if (filter_type in spells[s] and spells[s][filter_type] == filter_criterion)]
        return {spell:spells[spell] for spell in spell_names}

    def identify(self, spell):
        if (spell is "" and not spell in self.spells):
            return
        print('\n{0}\n=========='.format(spell))
        for key in self.spells[spell]:
            print('{0}: {1}'.format(key,self.spells[spell][key]))
