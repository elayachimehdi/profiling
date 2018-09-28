############################ Description des scipts : 
 - preprocessing : Fichier principal pour la transformation de la bas de données 
 - fonctions : contient les fonctions à utiliser pour le script
 - parametres : contient la majorité des paramètres à modifier dans le programme
 - kmeans : son nom indique à quoi il sert. Pour extraire le dataframe avec les classe du cluster, il faut importer la fonction "main" depuis n'importe quel autre script dans le meme dossier. (main ne prend aucun parametre, tous les parametres sont dans le fichier kmeans)
 - importations : toujours en phase de développement, c'est pour centraliser l'importations des données 
 - data_preprocessing : fichier pour la transformation du questionnaire pour le clustering

############################ Preprocessing : 
dbase_montant_brut : Table des montants de chaque type de transactions par client et années (Montant_Total)
dbase_pourcentage_client : Table des pourcentages de chaque type de transactions par client et année
dbase_risque_client : Table des profils de risque issus du clustering par client
dbase_montant_risque_volume :Table des volumes echangés par profil de risque (VolumeTotal)
dbase_montant_risque_qte : Table des quantités échangées par profil de risque (QteTotale)
dbase_pourcentage_risque_volume : Table des pourcentages (en terme de volume échangé) par profil de risque
dbase_pourcentage_risque_qte : Table des pourcentages (en terme de quantité échangée) par profil de risque