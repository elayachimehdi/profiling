'''Avant de lancer le script il faut metter sa console sur le dossier profiling (master branch)'''

#Recupérer la reponse ou le client defini son profil 


#Importation des librairies
import pyodbc as db
import pandas as pd
import numpy as np


#Initialisation de la connection
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
#cur = con.cursor()



#Requete pour extraire les réponses au questionnaire (Table  KYC)
df = pd.read_sql('SELECT * FROM Peaqock.dbo.KYC',con)
#Requete pour extraire les questions du questionnaire (Table  Questionnaire)
questions = pd.read_sql('SELECT * FROM Peaqock.dbo.Questionnaire',con)



# Suppression des colonnes "vides" ####################################################################################################################################
from fonctions import del_columns, del_rows, index_to_question
questions_to_delete= [28,34,36]+list(range(38,44))  #Les questions de la validation du questionnaire
delete = index_to_question(questions_to_delete)
df = df.drop(delete,axis = 1)
df = del_columns(df)   #Les colonnes vides à 50%
df = del_rows(df)      #Les lignes vides à 50%



#Remplacement des chaines de caractère ####################################################################################################################################
from changements import OLD, NEW
df = df.replace(OLD,NEW)


#Imputation des données ####################################################################################################################################
from sklearn.preprocessing import Imputer
labels = df.columns
imptr = Imputer(missing_values= 'NaN', strategy = 'mean', axis = 0)
df = df.convert_objects(convert_numeric=True)
df = df.values
imptr.fit(df)
df = imptr.transform(df)
df = np.around(df)
df = pd.DataFrame(df, columns = labels)


#Scoring des données ##########################################################################################################################################
from fonctions import summer

#Connaissance du marché (questions : 1,2,3,4,5,7,9)
df[['Q2','Q3','Q4','Q5','Q7']] = df[['Q2','Q3','Q4','Q5','Q7']].multiply(5, axis = 1) 
df = summer(df, ['Q2','Q3','Q4','Q5','Q7'], label = 'instruments_connus')
df[['Q9']] = df[['Q9']].multiply(10, axis = 1) 
df = summer(df,['Q1','instruments_connus','Q9'], label = 'connaissance_marche')

#Tolerance au risque (questions : 10,11,12,13,14,19,20,29
df[index_to_question([10,14])] = df[index_to_question([10,14])].multiply(15, axis = 1) 
df[index_to_question([11,12,13])] = df[index_to_question([11,12,13])].multiply(5, axis = 1) 
df[index_to_question([29])] = df[index_to_question([29])].multiply(15, axis = 1) 
df = summer(df,index_to_question([10,11,12,13,14,19,20,29]), label = 'tolerance_risque')

#Situation patrimoniale (questions : 45 )
df[index_to_question([45])] = df[index_to_question([45])].multiply(15, axis = 1) 
df['situation_patrimoniale'] = df[index_to_question([45])]
df = df.drop(index_to_question([45]), axis=1)

#Horizon (questions : 26 )
df['horizon'] = df[index_to_question([26])]
df = df.drop(index_to_question([26]), axis=1)

#Objectif d'investissement(questions : 21,22,23,24,32 )
df[index_to_question([21])] = df[index_to_question([21])].multiply(15, axis = 1) 
df[index_to_question([22])] = df[index_to_question([22])].multiply(10, axis = 1) 
df[index_to_question([23])] = df[index_to_question([23])].multiply(5, axis = 1) 
df[index_to_question([24])] = df[index_to_question([24])].multiply(20, axis = 1) 
df = summer(df,index_to_question([21,22,23,24,32]), label = 'objectif_investissement')

#Temps disponible (question : 30)
df['temps_disponible'] = df[index_to_question([30])]
df = df.drop(index_to_question([30]), axis=1)

#Mode de gestion (question : 16,18)
table = np.array(df[['Q16','Q18']].values).T
scalar = table[0]*table[1]
df = df.drop(['Q16','Q18'], axis=1)
df['mode_gestion']=pd.DataFrame(scalar)





















