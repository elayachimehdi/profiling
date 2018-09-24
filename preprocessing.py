#Importation des librairies 
import pandas as pd 
import numpy as np 
from kmeans import main
import pyodbc as db 
import time


#Importation des parametres et des fonctions
from fonctions import year_index, quantifier, value_to_index,percenter, isin_index
from parametres import annees, all_id_TypeValeurs, all_label_TypeValeurs

#Importation des données 
timee = time.time()
print('Importation des données en cours ...')

con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
cur = con.cursor()
df = pd.read_sql("""SELECT * 
  FROM (((peaqock.dbo.TransactionsHist
  inner join Peaqock.dbo.OrdresHist  ON  Peaqock.dbo.TransactionsHist.IdOrdreEx = Peaqock.dbo.OrdresHist.IdOrdreEx)
      INNER join peaqock.dbo.ComptesEspece ON IdCompte=IdCompteEspece)
          INNER join Peaqock.dbo.Clients  ON IdClient=IdPersonne)""",con)

clustered = main()
clustered.index = clustered.IdPersonne
Id_Personne_KYC = list(set(clustered.IdPersonne))
data = pd.DataFrame()
for ix in Id_Personne_KYC :
    if data.empty :
        data = df[df['IdPersonne'] == ix]
    else :
        data = pd.concat([df[df['IdPersonne'] == ix],data])

#df = pd.read_csv('./clients_questionnaire.csv')
#df = df.drop('Unnamed: 0',axis = 1)

df = data

print('Importation des données terminée.',int(time.time() - timee))

##Suppression des variables inutiles ou vides 
#list_to_drop = ['Unnamed: 0','IdPersonne','IdCompteEspece','IdOrdreEx','CodeRejet','PrixStop','Marge','QteMinimale','QteDevoilee','NamedOrder','StatusOrdre']
#df = df.drop(list_to_drop,axis = 1)





#Ajout de features
df['TypeValeur'] = df['IdTypeValeur'].replace(all_id_TypeValeurs,all_label_TypeValeurs)



#%%Extraction des montants Brut pour chaque annee pour chaque client 
# Base de données : dbase_montant_brut

print('Création des Dataframes')



#Initiation des bases de données de sortie
clients = list(set(df.IdClient))
profils = list(set(clustered.classe))
columns_montants_brut = all_label_TypeValeurs+['Montant_Total']
columns_pourcentage = all_label_TypeValeurs
columns_risque = ['ProfilRisque']
row_index = pd.MultiIndex.from_product([clients,annees], names = ['client','annee'])
dbase_montant_brut = pd.DataFrame(np.ones((len(clients)*len(annees),len(columns_montants_brut))), columns= columns_montants_brut, index =row_index )
dbase_pourcentage_client = pd.DataFrame(np.ones((len(clients)*len(annees),len(columns_pourcentage))), columns = columns_pourcentage, index =row_index )
dbase_risque_client = pd.DataFrame(np.ones(len(clients)), columns = columns_risque,index = clients)
dbase_montant_risque_volume = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs)+1)),columns = all_label_TypeValeurs+['VolumeTotal'], index = profils)
dbase_montant_risque_qte = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs)+1)),columns = all_label_TypeValeurs+['QteTotale'], index = profils)
dbase_pourcentage_risque_volume = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs))),columns = all_label_TypeValeurs, index = profils)
dbase_pourcentage_risque_qte = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs))),columns = all_label_TypeValeurs, index = profils)



verify =[]
evolution = -1

for idclient in clients :
    print(idclient)
    current_evolution = int(((list(clients).index(idclient)+1)/len(clients))*10)*10
    if current_evolution != evolution :
        evolution = current_evolution 
        print(str(evolution)+'%', end = '  ')
    
    transactions_client = df[df['IdClient'] == idclient]
    
    profil_de_risque = clustered['Score_classe'][idclient]
    dbase_risque_client.ProfilRisque[idclient] =  profil_de_risque
    montants_risque_volume = list(quantifier(transactions_client,'TypeValeur', 'MontantBrut',all_label_TypeValeurs).iloc[0])
    dbase_montant_risque_volume.loc[profil_de_risque] += montants_risque_volume + [sum(montants_risque_volume)]
    montants_risque_qte = list(quantifier(transactions_client,'TypeValeur', 'QteTitre',all_label_TypeValeurs).iloc[0])
    dbase_montant_risque_qte.loc[profil_de_risque] += montants_risque_qte + [sum(montants_risque_qte)]
    
    
    
    for annee in annees :
        transactions_annee_client = transactions_client[year_index(transactions_client.StatusDate, annee)]
        list1 = value_to_index(list(quantifier(transactions_annee_client,'TypeValeur', 'MontantBrut',all_label_TypeValeurs).iloc[0]))
        list2 = list(set(transactions_annee_client.TypeValeur))
        for element in list2 :
            if element not in list1 :
                verify.append(element)

        montants_transactions = list(quantifier(transactions_annee_client,'TypeValeur', 'MontantBrut',all_label_TypeValeurs).iloc[0])
        dbase_montant_brut.loc[(idclient,annee)] = montants_transactions + [sum(montants_transactions)]
        dbase_pourcentage_client.loc[(idclient,annee)] = percenter(montants_transactions)
        
print('\n Dataframes crées et remplis')
        






################################################################################### to do list ##########################################
#Change the date slicing function























