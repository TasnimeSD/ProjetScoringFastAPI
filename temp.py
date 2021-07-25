import json
def open_file():
    with open('input.json',encoding='utf8') as json_data:
        return json.load(json_data)

def update_json(y):     
    with open('input.json') as json_file: 
        contenu = json.load(json_file)    
        contenu.append(y)     
    write_json(contenu)

def write_json(data): 
    with open('input.json','w') as f: 
        json.dump(data, f, indent=4)

Test =  {"id": -1,
        "Nom": "Hannachi",
        "Prenom": "Moez",
        "Zone": "Sud",
        "Age_rel": "20",
        "Mnt_crd":"10000",
        "Val_Gar":"20000",
        "Sexe":"Femme",
        "Marche":"",
        "Segment":""}

for x in range(250000):
        Test["id"]=457323 + x +1
        Test["Sexe"]= "Femme"
        Test["Zone"]="Nord"
        Test["Marche"]= "PAR"
        Test["Segment"]= "2"
        Test["Mnt_crd"]= 150000
        Test["Age_rel"]=20
        Test["Val_Gar"]=150000

update_json(Test)