'''Used to lock down sensitive information before pushing to github'''

from KeyLoader import KeyLoader
import os, json

keyloader = KeyLoader()
password = input('Please enter a password:  ')
unlocked_files = [f for f in os.listdir('data/unlocked') if '.json' in f]
for f in unlocked_files:
    unlocked_data = json.load(open('data/unlocked/' + f,'r'))
    locked_data = keyloader.lockWithPassword(password, json.dumps(unlocked_data).encode('utf-8'))
    print('{0} locked and deleted'.format(f))
    with open('data/locked/{0}'.format(f),'wb') as f_out:
    	f_out.write(locked_data)
    os.remove('data/unlocked/' + f)
