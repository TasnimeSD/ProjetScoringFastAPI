from fastapi import FastAPI#, Request
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
#from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import pickle
import numpy as np
import aiofiles
import json
import datetime

# initialization
app = FastAPI()

# mount static folder to serve static files
#app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 template instance for returning webpage via template engine
templates = Jinja2Templates(directory="templates")

model = pickle.load(open('model.pkl' , 'rb'))

def write_json(data): 
    with open('output.json','w') as f: 
        json.dump(data, f, indent=4)

def open_file():
    with open('input.json',encoding='utf8') as json_data:
        return json.load(json_data)

def update_json(y):     
    with open('output.json') as json_file: 
        contenu = json.load(json_file)    
        contenu.append(y)     
    write_json(contenu)

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

global Test

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


def calcul_score():
    ##Récupération des valeurs à partir du formulaire
    dictionnaire= Request.form.values()
    data=list(dictionnaire)
    
    data.pop(0)
    data.pop(0)
    int_features = [int(x) for x in data]
    LTV=int_features[len(int_features)-2]*100/int_features[len(int_features)-1]
    int_features=int_features[:-2]+[LTV]
    final = [np.array(int_features)]
    #Calcul du score
    prediction = model.predict_proba(final)
    score= '{0:.{1}f}'.format((prediction[0][1])*100, 2)
    return score

Test =  {"id": -1,
        "Nom": "",
        "Prenom": "",
        "Zone": "",
        "Age_rel": "",
        "Mnt_crd":"",
        "Val_Gar":"",
        "Sexe":"",
        "Marche":"",
        "Segment":""}

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/")#, response_class=HTMLResponse)
def index(): #request: Request
    #Initialisation du formulaire
    global a
    a=-1
    Test =  {"id": -1,
        "Nom": "",
        "Prenom": "",
        "Zone": "",
        "Age_rel": "",
        "Mnt_crd":"",
        "Val_Gar":"",
        "Sexe":"",
        "Marche":"",
        "Segment":""}
    return FileResponse("templates/index.html")
    #return templates.TemplateResponse("index.html") #, {"request": request}


@app.post('/ref')
def ref():
    global a
    if 'id' in Request.args:
        id = int(Request.args['id'])
        a=id
        Test=extract_ref(id)
    print("post(ref)")
    Test =modif_contenu(Test)
    return FileResponse("templates/index.html")


#@app.route('/predict' , methods=['POST','GET'])
@app.post('predict')
async def predict(request: Request):
    if Request.method == 'POST':
        #Test1 = request.form
        form = await request.form()
        Test["id"]=a
        Test["Sexe"]= form['Sexe']
        Test["Zone"]= form['Zone']
        Test["Marche"]= form['Marche']
        Test["Segment"]= form['Segment']
        Test["Mnt_crd"]= form['Mnt_crd']
        Test["Age_rel"]=form['Age_rel']
        Test["Val_Gar"]=form['Val_Gar']
        Test["Nom"]=form['Nom']
        Test["Prenom"]=form['Prenom']

    if Test["id"]>=0:    
        dateMJ = datetime.datetime.now()
        Test["score"]= calcul_score()
        Test["Date"]= str(dateMJ)
        Test["IP"]=request.remote_addr
        update_json(Test)
    print("post(predict)")
    if calcul_score()>str(50):
        #return render_template('Index.html',Test=modif_contenu(Test), pred="Risque élevé.\n Le score attribué à cette demande est {}".format(calcul_score())+"/100")
        return FileResponse("templates/index.html", pred="Risque élevé.\n Le score attribué à cette demande est {}".format(calcul_score())+"/100")
        #return {'result': calcul_score()}

    else:
        #return render_template('Index.html',Test=modif_contenu(Test),  pred="Risque faible.\n Le score attribué à cette demande est {}".format(calcul_score())+"/100")
        return FileResponse("templates/index.html", pred="Risque faible.\n Le score attribué à cette demande est {}".format(calcul_score())+"/100")
        #return templates.TemplateResponse('Index.html', context={'request': Request, 'result': calcul_score()})
        #return {'result': calcul_score()}

    #return {"result": calcul_score()}
    # Export les données en json  avec la date et le score calculé=> Partie en cours d'optimisation


if __name__ == '__main__':   
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
