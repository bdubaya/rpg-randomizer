'''Used to unlock sensitive information after pulling from github'''

from KeyLoader import KeyLoader
from collections import OrderedDict
import os, json

keyloader = KeyLoader()
password = input('Please enter your password:  ')

# Get lists of bothlocked files and unlocked files
locked_files = [f for f in os.listdir('data/locked') if '.json' in f]
unlocked_files = [f for f in os.listdir('data/unlocked') if '.json' in f]

for f in locked_files:
    if f in unlocked_files:
        contin = input('Conflict in {0}, do you wish to overwrite? (Y/n)  '.format(f))
        if (contin == 'n' or contin == 'N'):
            continue

    print('Writing {0}'.format(f))
    with open('data/locked/' + f,'rb') as infile:
        full_data = infile.read()

    unlocked_data = keyloader.unlock_with_password(password, full_data)
    with open('data/unlocked/' + f,'w') as f_out:
        ordered = OrderedDict(sorted(unlocked_data.items(), key=lambda t: t[0]))
        json.dump(ordered, f_out)
