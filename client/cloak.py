import json
import random

# load settings
settings = json.load(open('server/settings.json'))
app_cats = settings['a']    
ufs = settings['u']
contexts = settings['c']

actions = settings['k']

# generate lists
al = [i for i in range(app_cats)]
ul = [i for i in range(ufs)]
cl = [i for i in range(contexts)]

kl = [i for i in range(actions)]

# shuffle lists
random.shuffle(al)
random.shuffle(ul)
random.shuffle(cl)

random.shuffle(kl)

# create key
key = dict()
key['app_cats'] = al
key['ufs'] = ul
key['contexts'] = cl

key['actions'] = kl

# save key
json.dump(key, open('client/key.json', 'w'))