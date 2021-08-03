import json


def open_file():
    # returns (load) all clients in input.json as a list of clients
    with open('input.json',encoding='utf8') as json_data:
        return json.load(json_data)

def write_json(data): 
    with open('output.json','w') as f: 
        json.dump(data, f, indent=4)

def update_json(y):     
    with open('output.json') as json_file: 
        contenu = json.load(json_file)    
        contenu.append(y)     
    write_json(contenu)

## Modifier le contenu de formulaire : conversion en (int)
def modif_contenu(Test):
    if (Test['Sexe']=="Homme" or str(Test['Sexe'])=="0"):
        Test["Sexe"] = 0
    elif (Test["Sexe"] == "Femme" or str(Test['Sexe']) == "1"):
        Test["Sexe"] = 1
    else:
        Test["Sexe"] = -1
    ##Conversion de la zone
    if (Test['Zone'] == "Nord" or str(Test['Zone']) == "0"):
        Test["Zone"] = 0
    elif (Test["Zone"] == "Centre" or str(Test['Zone']) == "1"):
        Test["Zone"] = 1
    elif (Test["Zone"] == "Sud" or str(Test['Zone']) == "2"):
        Test["Zone"] = 2
    else:
        Test["Zone"] = -1
    ##Conversion du marché
    if (Test['Marche'] == "PRF" or str(Test['Marche']) =="0"):
        Test["Marche"] = 0
    elif (Test["Marche"] == "PAR" or str(Test['Marche']) == "1"):
        Test["Marche"] = 1
    else:
        Test["Marche"] = -1

    #Conversion Segment
    if(Test['Segment'] == "Autres Professions Libérales" or str(Test['Segment']) =="0"):
        Test["Segment"] = 0
    elif (Test["Segment"] == "Dirigeants d'Entreprises Salariés Privé" or str(Test['Segment']) =="1"):
        Test["Segment"] = 1
    elif (Test["Segment"] == "TRE/artisans/commerçants/prof libérales" or str(Test['Segment']) =="2"):
        Test["Segment"] = 2
    elif (Test["Segment"] == "salariés privés" or str(Test['Segment']) =="3"):
        Test["Segment"] = 3
    elif (Test["Segment"] == "Etudiants/rentiers/autres" or str(Test['Segment']) =="4"):
        Test["Segment"] = 4
    elif (Test["Segment"] == "Médecins et assimilés" or str(Test['Segment']) =="5"):
        Test["Segment"] = 5
    elif (Test["Segment"] == "salariés public" or str(Test['Segment']) =="6"):
        Test["Segment"] = 6
    elif (Test["Segment"] == "commerçants" or str(Test['Segment']) =="7"):
        Test["Segment"] = 7
    elif (Test["Segment"] == "Professions libérales" or str(Test['Segment']) =="8"):
        Test["Segment"] = 8
    elif (Test["Segment"] == "Artisans" or str(Test['Segment']) =="9"):
        Test["Segment"] = 9
    elif (Test["Segment"] == "Avocats et assimilés" or str(Test['Segment']) =="10"):
        Test["Segment"] = 10
    elif (Test["Segment"] == "Retaités" or str(Test['Segment']) =="11"):
        Test["Segment"] = 11
    else:
        Test["Segment"] = -1
    
    return Test


#get client by id
def extract_ref(id):
    list = []
    credit_refs = open_file()
    for credit_ref in credit_refs:
        if credit_ref['id'] == id:
            list.append(credit_ref)

    Remove_list=str(list).strip('[]')
    with_quots = Remove_list.replace("\'", "\"")
    Test=json.loads(with_quots)

    Test=modif_contenu(Test)
    return Test


