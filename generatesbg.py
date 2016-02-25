from objects.SpellBookGenerator import *
sbg = SpellBookGenerator()
book = sbg.create_list('Wizard',['Evocation','Illusion','Abjuration','Transmutation'],[5,4,3,3,2])
print(book)
