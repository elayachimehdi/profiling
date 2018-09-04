#Importation des librairies
import pyodbc as db
import pandas as pd


#Initialisation de la connection
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
#cur = con.cursor()

#Requete pour extraire les réponses au questionnaire (Table  KYC)
query_kyc='SELECT * FROM Peaqock.dbo.KYC'
df_kyc = pd.read_sql(query_kyc,con)

# Nettoyage du Dataframe KYC

#Q1
q1 = df_kyc.iloc[:,[0]]





#Insider functions ##############################################################################################

def adaptor(df,old_values, new_values) :
    if len(old_values) != len(new_values) :
        print("The length of the lists don't match !")
    else :
        for column_index in range(len(df.columns)) :
            print('column : '+str(column_index))
            for row_index in range(len(df.iloc[:,[column_index]])) :
                print('row : '+str(row_index))
                if df.iloc[row_index,[column_index]] in old_values :
                    ix = old_values.index(df.iloc[row_index,[column_index]])
                    print('Index taken')
                    df.iloc[row_index,[column_index]] = new_values[ix]
        return df
                    











