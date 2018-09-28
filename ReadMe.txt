############################ Description des scipts : 
 - preprocessing : Fichier principal pour la transformation de la bas de donn�es 
 - fonctions : contient les fonctions � utiliser pour le script
 - parametres : contient la majorit� des param�tres � modifier dans le programme
 - kmeans : son nom indique � quoi il sert. Pour extraire le dataframe avec les classe du cluster, il faut importer la fonction "main" depuis n'importe quel autre script dans le meme dossier. (main ne prend aucun parametre, tous les parametres sont dans le fichier kmeans)
 - importations : toujours en phase de d�veloppement, c'est pour centraliser l'importations des donn�es 
 - data_preprocessing : fichier pour la transformation du questionnaire pour le clustering

############################ Preprocessing : 
dbase_montant_brut : Table des montants de chaque type de transactions par client et ann�es (Montant_Total)
dbase_pourcentage_client : Table des pourcentages de chaque type de transactions par client et ann�e
dbase_risque_client : Table des profils de risque issus du clustering par client
dbase_montant_risque_volume :Table des volumes echang�s par profil de risque (VolumeTotal)
dbase_montant_risque_qte : Table des quantit�s �chang�es par profil de risque (QteTotale)
dbase_pourcentage_risque_volume : Table des pourcentages (en terme de volume �chang�) par profil de risque
dbase_pourcentage_risque_qte : Table des pourcentages (en terme de quantit� �chang�e) par profil de risque