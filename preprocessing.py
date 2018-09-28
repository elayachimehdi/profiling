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

#con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
#cur = con.cursor()
#df = pd.read_sql("""SELECT * 
#  FROM (((peaqock.dbo.TransactionsHist
#  inner join Peaqock.dbo.OrdresHist  ON  Peaqock.dbo.TransactionsHist.IdOrdreEx = Peaqock.dbo.OrdresHist.IdOrdreEx)
#      INNER join peaqock.dbo.ComptesEspece ON IdCompte=IdCompteEspece)
#          INNER join Peaqock.dbo.Clients  ON IdClient=IdPersonne)""",con)
#

#Id_Personne_KYC = list(set(clustered.IdPersonne))
#data = pd.DataFrame()
#for ix in Id_Personne_KYC :
#    if data.empty :
#        data = df[df['IdPersonne'] == ix]
#    else :
#        data = pd.concat([df[df['IdPersonne'] == ix],data])
#df = data


df = pd.read_csv('./clients_questionnaire.csv')
df = df.drop('Unnamed: 0',axis = 1)

clustered = main()
clustered.index = clustered.IdPersonne

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
row_index = pd.MultiIndex.from_product([clients,annees], names = ['client','annee'])



dbase_montant_brut = pd.DataFrame(np.ones((len(clients)*len(annees),len(all_label_TypeValeurs+['Montant_Total']))), columns= all_label_TypeValeurs+['Montant_Total'], index =row_index )
dbase_qte_brut = pd.DataFrame(np.ones((len(clients)*len(annees),len(all_label_TypeValeurs+['Qte_Total']))), columns= all_label_TypeValeurs+['Qte_Total'], index =row_index )
dbase_pourcentage_client = pd.DataFrame(np.ones((len(clients)*len(annees),len(all_label_TypeValeurs))), columns = all_label_TypeValeurs, index =row_index )
dbase_risque_client = pd.DataFrame(np.ones(len(clients)), columns = ['ProfilRisque'],index = clients)
dbase_montant_risque_volume = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs)+1)),columns = all_label_TypeValeurs+['VolumeTotal'], index = profils)
dbase_montant_risque_qte = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs)+1)),columns = all_label_TypeValeurs+['QteTotale'], index = profils)
dbase_pourcentage_risque_volume = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs))),columns = all_label_TypeValeurs, index = profils)
dbase_pourcentage_risque_qte = pd.DataFrame(np.zeros((len(profils),len(all_label_TypeValeurs))),columns = all_label_TypeValeurs, index = profils)



dbase_risque_annee = pd.DataFrame(np.zeros((len(annees),len(profils))), columns = profils, index = annees)
dbase_profil_risque = pd.DataFrame(np.zeros((1,3)), columns = profils)
dbase_equilibre_vq = pd.DataFrame(np.zeros((2,len(all_label_TypeValeurs)+2)), columns = all_label_TypeValeurs+['Total', 'Type'] )
dbase_prudent_vq = pd.DataFrame(np.zeros((2,len(all_label_TypeValeurs)+2)), columns = all_label_TypeValeurs+['Total', 'Type'] )
dbase_risque_vq = pd.DataFrame(np.zeros((2,len(all_label_TypeValeurs)+2)), columns = all_label_TypeValeurs+['Total', 'Type'] )
dbase_risque_volume = pd.DataFrame(np.zeros((len(all_label_TypeValeurs),len(profils))), columns = profils , index = all_label_TypeValeurs)



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
    dbase_profil_risque.loc[0,profil_de_risque] += 1
    
    
    
    
    for annee in annees :
        transactions_annee_client = transactions_client[year_index(transactions_client.StatusDate, annee)]
        list1 = value_to_index(list(quantifier(transactions_annee_client,'TypeValeur', 'MontantBrut',all_label_TypeValeurs).iloc[0]))
        list2 = list(set(transactions_annee_client.TypeValeur))
        for element in list2 :
            if element not in list1 :
                verify.append(element)

        montants_transactions = list(quantifier(transactions_annee_client,'TypeValeur', 'MontantBrut',all_label_TypeValeurs).iloc[0])
        dbase_montant_brut.loc[(idclient,annee)] = montants_transactions + [sum(montants_transactions)]
        qte_transactions = list(quantifier(transactions_annee_client,'TypeValeur', 'QteTitre',all_label_TypeValeurs).iloc[0])
        dbase_qte_brut.loc[(idclient,annee)] = qte_transactions + [sum(qte_transactions)]
        dbase_pourcentage_client.loc[(idclient,annee)] = percenter(montants_transactions)
        dbase_risque_annee.loc[annee,profil_de_risque] += sum(montants_transactions)
        


        

#%%################################################################################## Statique ###########################################

dbase_prudent_vq.loc[0] = list(dbase_montant_risque_volume.loc['Prudent'])+['Volume']
dbase_equilibre_vq.loc[0] = list(dbase_montant_risque_volume.loc['Equilibré'])+['Volume']
dbase_risque_vq.loc[0]= list(dbase_montant_risque_volume.loc['Risqué'])+['Volume']


dbase_prudent_vq.loc[1] = list(dbase_montant_risque_qte.loc['Prudent'])+['Qte']
dbase_equilibre_vq.loc[1] = list(dbase_montant_risque_qte.loc['Equilibré'])+['Qte']
dbase_risque_vq.loc[1]= list(dbase_montant_risque_qte.loc['Risqué'])+['Qte']

dbase_risque_volume['Prudent'] = list(dbase_montant_risque_volume.loc['Prudent'])[:-1]
dbase_risque_volume['Equilibré'] = list(dbase_montant_risque_volume.loc['Equilibré'])[:-1]
dbase_risque_volume['Risqué'] = list(dbase_montant_risque_volume.loc['Risqué'])[:-1]



print('\n Dataframes crées et remplis')

#%%################################################################################## to do list ##########################################
#Change the date slicing function


#%%################################################################################## Inserting into DB ##########################################


from fonctions import separator, execom, insert
from parametres import col_mb, col_mrq, col_mrv, col_pc, col_prq, col_prv, col_rc, col_ra, col_pr, col_vq, col_rv
import pymysql as my

con = my.connect(host='localhost', user = 'root', db = 'ckb_profiling')

dbase_montant_brut = separator(dbase_montant_brut,['IdPersonne','annee'])
dbase_pourcentage_client = separator(dbase_pourcentage_client,['IdPersonne','annee'])
dbase_risque_client = separator(dbase_risque_client, ['IdPersonne'])
dbase_montant_risque_qte = separator(dbase_montant_risque_qte, ['Profil_Risque'])
dbase_pourcentage_risque_qte = separator(dbase_pourcentage_risque_qte, ['Profil_Risque'])
dbase_montant_risque_volume = separator(dbase_montant_risque_volume, ['Profil_Risque'])
dbase_pourcentage_risque_volume = separator(dbase_pourcentage_risque_volume, ['Profil_Risque'])

dbase_risque_annee = separator(dbase_risque_annee,['Année'])
dbase_risque_volume = separator(dbase_risque_volume,['Type'])






execom(insert('montant_brut', dbase_montant_brut, col_mb),con)
execom(insert('montant_risque_qte', dbase_montant_risque_qte, col_mrq),con)
execom(insert('montant_risque_volume', dbase_montant_risque_volume, col_mrv),con)
execom(insert('pourcentage_client', dbase_pourcentage_client, col_pc),con)
execom(insert('pourcentage_risque_qte', dbase_pourcentage_risque_qte, col_prq),con)
execom(insert('pourcentage_risque_volume', dbase_pourcentage_risque_volume, col_prv),con)
execom(insert('risque_client', dbase_risque_client, col_rc),con)

execom(insert('risque_annee', dbase_risque_annee, col_ra),con)
execom(insert('profil_risque', dbase_profil_risque, col_pr),con)
execom(insert('equilibre_vq', dbase_equilibre_vq, col_vq),con)
execom(insert('risque_vq', dbase_risque_vq, col_vq),con)
execom(insert('prudent_vq', dbase_prudent_vq, col_vq),con)
execom(insert('risque_volume', dbase_risque_volume, col_rv),con)












