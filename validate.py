import json

spells = json.load(open('data/unlocked/spells.json','r'))

# Let's get an example with EVERYTHING completed
example = spells['Aid']

for field in example:
    spells_missing_field = [s for s in spells if field not in spells[s]]
    if len(spells_missing_field) > 0:
        missing_list = ', '.join(spells_missing_field)
        print("The following {2} spells are missing the '{0}' field.\n\n{1}\n\n".format(field, missing_list, len(spells_missing_field)))

# Validate Entries
characterdata = json.load(open('data/unlocked/character.json','r'))
classes = characterdata['npc']['playable_class']
schools = ['Abjuration','Conjuration','Divination','Enchantment','Evocation','Illusion','Necromancy','Transmutation']

# Validate Fields
for spell in spells:
    invalid_field = [field for field in spells[spell] if field not in example]
    for field in invalid_field:
        print("Spell '{0}' has erroneous field '{1}'".format(spell,field))

    if 'classes' in spells[spell]:
        invalid_classes = [c for c in spells[spell]['classes'] if c not in classes]
        for c in invalid_classes:
            print("Spell '{0}' has erroneous class '{1}'".format(spell,c))

    if 'school' in spells[spell]:
        if spells[spell]['school'] not in schools:
            print("Spell '{0}' has erroneous school '{1}'".format(spell, spells[spell]['school']))
