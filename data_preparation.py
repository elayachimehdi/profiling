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

questions_to_delete= [34,36]+list(range(38,44))  #Les questions de la validation du questionnaire
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
from fonctions import scorer
df = scorer(df)


#Récupération de l'output de vérification
from fonctions import categoriser
output = categoriser(s = df['Q28'], labels = ['Prudent','Equilibré', 'Dynamique','Offensif'], no_drop =True )
#output = pd.DataFrame(df['Q28'])
df = df.drop(['IdPersonne','Q28'],axis = 1)


# Standardisation
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
df = sc.fit_transform(df)

#



















