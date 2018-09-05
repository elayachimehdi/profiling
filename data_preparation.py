'''Avant de lancer le script il faut metter sa console sur le dossier profiling (master branch)'''
#Importation des librairies
import pyodbc as db
import pandas as pd
import numpy as np


#Initialisation de la connection
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
#cur = con.cursor()

#Requete pour extraire les réponses au questionnaire (Table  KYC)
query_kyc='SELECT * FROM Peaqock.dbo.KYC'
df = pd.read_sql(query_kyc,con)
#Requete pour extraire les questions du questionnaire (Table  Questionnaire)
'''query_questionnaire='SELECT * FROM Peaqock.dbo.Questionnaire'
questions = pd.read_sql(query_questionnaire,con)'''

# Suppression des colonnes "vides"
from fonctions import del_columns, del_rows
df = del_columns(df)
df = del_rows(df)


#Remplacement des chaines de caractère
from changements import OLD, NEW
df = df.replace(OLD,NEW)

#Imputation des données
from sklearn.preprocessing import Imputer
labels = df.columns
imptr = Imputer(missing_values= 'NaN', strategy = 'mean', axis = 0)
df = df.convert_objects(convert_numeric=True)
df = df.values
imptr.fit(df)
df = imptr.transform(df)
df = np.around(df)
df = pd.DataFrame(df, columns = labels)


#Les variables catégoriques 
from fonctions import categoriser
from changements import Q36_old,Q45_old
df = categoriser(dataframe = df, index = df.columns.get_loc('Q36'), labels = Q36_old)
df = categoriser(dataframe = df, index = df.columns.get_loc('Q45'), labels = Q45_old)










"""
'''Avant de lancer le script il faut metter sa console sur le dossier profiling (master branch)'''
#Importation des librairies
import pyodbc as db
import pandas as pd


#Initialisation de la connection
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
#cur = con.cursor()

#Requete pour extraire les réponses au questionnaire (Table  KYC)
query_kyc='SELECT * FROM Peaqock.dbo.KYC'
df = pd.read_sql(query_kyc,con)

#Requete pour extraire les réponses au questionnaire (Table  KYC)
query_questionnaire='SELECT * FROM Peaqock.dbo.Questionnaire'
questions = pd.read_sql(query_questionnaire,con)


# Nettoyage du Dataframe KYC
from fonctions import index_to_question
Nulls = pd.DataFrame(df.isnull().sum())
seuil = len(df)/2
to_delete = [i for i in range(len(Nulls)) if Nulls[0][i]>seuil]
df = df.drop(index_to_question(to_delete), axis = 1)


#Remplacment
from changements import OLD, NEW
df = df.replace(OLD,NEW)

"""






