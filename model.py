#!C:\Users\Asus\AppData\Local\Programs\Python\Python37-32\python.exe

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import warnings
import pickle
warnings.filterwarnings("ignore")

import pandas as pd

data = pd.read_excel (r'scoring.xlsx')
#print (data)

########Conversion du Sexe
data['Sexe_Id']=data['SEXE'].factorize()[0]
sexe_id_df=data[['SEXE','Sexe_Id']].drop_duplicates().sort_values('Sexe_Id')
sexe_to_id=dict(sexe_id_df.values)
id_to_sexe=dict(sexe_id_df[['Sexe_Id','SEXE']].values)

#print(data.head(5))
#####"Conversion de la zone géographique

data['Zone_geo_Id']=data['Zone_geo'].factorize()[0]
zone_id_df=data[['Zone_geo','Zone_geo_Id']].drop_duplicates().sort_values('Zone_geo_Id')
zone_to_id=dict(zone_id_df.values)
id_to_zone=dict(zone_id_df[['Zone_geo_Id','Zone_geo']].values)

#print(data.head(5))

########conversion marche
data['MARCHE_Id']=data['MARCHE'].factorize()[0]
MARCHE_id_df=data[['MARCHE','MARCHE_Id']].drop_duplicates().sort_values('MARCHE_Id')
MARCHE_to_id=dict(MARCHE_id_df.values)
id_to_MARCHE=dict(MARCHE_id_df[['MARCHE_Id','MARCHE']].values)

#print(data.head(5))

######conversion Segment
data['Nouv_SM_Id']=data['Nouv_SM'].factorize()[0]
Nouv_SM_id_df=data[['Nouv_SM','Nouv_SM_Id']].drop_duplicates().sort_values('Nouv_SM_Id')
Nouv_SM_to_id=dict(Nouv_SM_id_df.values)
id_to_Nouv_SM=dict(Nouv_SM_id_df[['Nouv_SM_Id','Nouv_SM']].values)

#print(data.head(5))



#data.to_csv("C:\Projet-Scoring\Scoring en flask\MyData_Transformed.csv")

dataF=data[['Anc_rel','Zone_geo_Id','Sexe_Id','MARCHE_Id','Nouv_SM_Id','Mnt_crd']]

y=data[['defaut']]
X = dataF
dataF = np.array(dataF)
#print(dataF)

print(data.Zone_geo_Id.unique())
print(data.MARCHE_Id.unique())
print(data.Nouv_SM_Id.unique())
print(data.Nouv_SM.unique())

y = y.astype('int')
X = X.astype('int')

#_train, y_train= train_test_split(X, y, random_state=0)
log_reg = LogisticRegression()

result=log_reg.fit(X,y)


#inputt = [int(x) for x in "200 3 1 2 5 100000".split(' ')]
#final = [np.array(inputt)]
#b = log_reg.predict_proba(final)

#print(b)

pickle.dump(log_reg, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))

#from joblib import dump
#dump(log_reg, 'model.joblib')


