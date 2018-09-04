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
Nulls = df.isnull().sum()

#Remplacment
from changements import OLD, NEW
df = df.replace(OLD,NEW)














#Insider functions ##############################################################################################







