from fastapi import FastAPI, Request, Form, APIRouter
#from starlette.requests import Request
from fastapi.templating import Jinja2Templates
#from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import pickle
import joblib
import numpy as np
import aiofiles
import json
import datetime
from pydantic import BaseModel
import time
import database

# initialization
app = FastAPI()

# mount static folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 template instance for returning webpage via template engine
templates = Jinja2Templates(directory="templates")

#Load the pretrained model
model = joblib.load(open('model.pkl' , 'rb')) 

class Test(BaseModel):
    id : int = -1
    Nom: str
    Prenom: str
    Zone: str
    Age_rel: str
    Mnt_crd: str 
    Val_Gar: str
    Sexe: str
    Marche: str
    Segment: str

#global Test
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

@app.get("/")
async def index(request : Request): 
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
    
    Test = database.modif_contenu(Test)
    return templates.TemplateResponse('index.html', {"request": request, "Test": Test})


@app.get("/ref/{id}")
async def ref(id: int, request: Request):
    global a
    id = int(id)
    Test=database.extract_ref(id)
    a = Test['id']
    Test = database.modif_contenu(Test)
    return templates.TemplateResponse('Index.html', {"request": request, "Test": Test})


#@app.route('/predict' , methods=['POST','GET'])
@app.post('/predict')
async def predict(request: Request):
    if request.method == 'POST':
        Test = {}
        form = await request.form()
        Test["id"]= a
        Test["Sexe"]= form['Sexe']
        Test["Zone"]= form['Zone']
        Test["Marche"]= form['Marche']
        Test["Segment"]= form['Segment']
        Test["Mnt_crd"]= form['Mnt_crd']
        Test["Age_rel"]=form['Age_rel']
        Test["Val_Gar"]=form['Val_Gar']
        Test["Nom"]=form['Nom']
        Test["Prenom"]=form['Prenom']
        
        Test = database.modif_contenu(Test)
        #calcul de score
        #create the features list for prediction
        data = [int(Test["Age_rel"]), int(Test["Zone"]), int(Test["Sexe"]),
        int(Test["Marche"]), int(Test["Segment"]), int(Test["Mnt_crd"]), int(Test["Val_Gar"])]
        int_features = [x for x in data]
        LTV=int_features[len(int_features)-2]*100/int_features[len(int_features)-1]
        int_features=int_features[:-2]+[LTV]
        final = [np.array(int_features)]
        #la prédiction du modele
        prediction = model.predict_proba(final)
        score= '{0:.{1}f}'.format((prediction[0][1])*100, 2)
        
    if Test["id"]>=0:    
        dateMJ = datetime.datetime.now()
        Test["score"]= score
        Test["Date"]= str(dateMJ)
        Test["IP"]=request.client.host 
        database.update_json(Test)
    # Export les données en json  avec la date , l'IP @ et le score calculé
    if score>str(50):
        msg = "Risque élevé.\n Le score attribué à cette demande est {}".format(score)+"/100"
        return templates.TemplateResponse("Index.html", {"request": request, "Test": Test, "pred": msg})
    else:
        msg = "Risque faible.\n Le score attribué à cette demande est {}".format(score)+"/100"
        return templates.TemplateResponse("Index.html", {"request": request, "Test": Test, "pred": msg})


if __name__ == '__main__':   
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)

