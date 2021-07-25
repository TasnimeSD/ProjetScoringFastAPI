import json
 
with open('superheroes.json') as f:
    superHeroSquad = json.load(f)
type(superHeroSquad)
# Output: dict
print(superHeroSquad.keys())
# Output: dict_keys(['squadName', 'homeTown', 'formed', 'secretBase', 'active', 'members'])

import pandas as pd
df = pd.read_json('superheroes.json')

#Affichage des données imbriquées
#Method 1
df['members'].apply(pd.Series)
df = pd.concat([df['members'].apply(pd.Series), df.drop('members', axis = 1)], axis = 1)
#Method 2
pd.json_normalize(superHeroSquad, record_path = ['members'], meta = ['squadName', 'homeTown', 'formed', 'secretBase', 'active'])
#Method 2 mais avec choix du préfixe
pd.json_normalize(superHeroSquad, record_path = ['members'], meta = ['squadName', 'homeTown', 'formed', 'secretBase', 'active'], meta_prefix = 'members_')

#Accéder aux valeurs: le résultat "Jane Wilson"
superHeroSquad['members'][1]['secretIdentity']

#Exporting from Python to JSON
#update secret identity of Eternal Flame
superHeroSquad['members'][2]['secretIdentity'] = 'Mahdi'
with open('superheroes.json', 'w') as file:
    json.dump(superHeroSquad, file)

#to export to JSON from Pandas Dataframe
df.to_json('superheroes.json')

#améliorer l'affichage du fichier Json
with open('superheroes.json', 'w') as file:
    json.dump(superHeroSquad, file, indent = 4)

#Effectuer un tri du fichier json
with open('superheroes.json', 'w') as file:
    json.dump(superHeroSquad, file, indent = 4, sort_keys = True)