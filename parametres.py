######################################################### Parametres ######################################################

list_to_drop = ['Unnamed: 0','IdPersonne','IdCompteEspece','IdOrdreEx','CodeRejet','PrixStop','Marge','QteMinimale','QteDevoilee','NamedOrder','StatusOrdre']
annees = list(range(2005,2019))

all_id_TypeValeurs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
all_label_TypeValeurs = ['Action Non Matérialisé',
 'Action Matérilisée',
 'Obligation Non Matérialisée',
 'Obligation Matérialisée',
 'Droit ',
 'TCN',
 'OPCVM ACTION',
 'OPCVM  Obligataire',
 'OPCVM Monétaire',
 'OPCVM Divesifiée Action ',
 'OPCVM Diversifiée Obligation',
 'BDP',
 'OR']


col_mb = ['Action_Non_Materialisée',
'Action_Materialisée',
'Obligation_Non_Materialisée',
'Obligation_Materialisée',
'Droit',
'TCN',
'OPCVM_ACTION',
'OPCVM_Obligataire',
'OPCVM_Monétaire',
'OPCVM_Divesifiée_Action',
'OPCVM_Diversifiée_Obligation',
'BDP',
'OR',
'Montant_Total',
'Id_Personne',
'Année']


create_table = ''' TABLE IF EXISTS `montant_brut`; CREATE TABLE IF NOT EXISTS `montant_brut` (`Index` int(11) NOT NULL,`Id_Personne` int(11) DEFAULT NULL,`Année` int(11) DEFAULT NULL,`ActionMatérilisée` double DEFAULT NULL,`Obligation_Non_Matérialisée` double DEFAULT NULL,`Obligation_Matérialisée` double DEFAULT NULL,`Droit` double DEFAULT NULL,`TCN` double DEFAULT NULL,`OPCVM_ACTION` double DEFAULT NULL,`OPCVM _Obligataire` double DEFAULT NULL,`OPCVM_Monétaire` double DEFAULT NULL,`OPCVM_Divesifiée_Action` double DEFAULT NULL,`OPCVM_Diversifiée_Obligation` double DEFAULT NULL,`BDP` double DEFAULT NULL,`OR` double DEFAULT NULL,`montant_total` double NOT NULL,PRIMARY KEY (`Index`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''


col_mrq =[ 'Action_Non_Materialisée',
 'Action_Materialisée',
 'Obligation_Non_Materialisée',
 'Obligation_Materialisée',
 'Droit',
 'TCN',
 'OPCVM_Obligataire',
 'OPCVM_ACTION',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Qte_Totale',
 'Profil_Risque']


col_mrv = [
 'Action_Non_Materialisée',
 'Action_Materialisée',
 'Obligation_Non_Materialisée',
 'Obligation_Materialisée',
 'Droit',
 'TCN',
 'OPCVM_ACTION',
 'OPCVM_Obligataire',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Volume_Total',
 'Profil_Risque']

col_pc = [
 'Action_Non_Materialisée',
 'Action_Materialisée',
 'Obligation_Non_Materialisée',
 'Obligation_Materialisée',
 'Droit',
 'TCN',
 'OPCVM_Obligataire',
 'OPCVM_ACTION',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Id_Personne',
 'Année']

col_prq = [ 
 'Action_Non_Materialisée',
 'Action_Materialisée',
 'Obligation_Materialisée',
 'Obligation_Non_Materialisée',
 'Droit',
 'TCN',
 'OPCVM_ACTION',
 'OPCVM_Obligataire',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Profil_Risque']

col_prv = [
 'Action_Non_Materialisée',
 'Action_Materialisée',
 'Obligation_Non_Materialisée',
 'Obligation_Materialisée',
 'Droit',
 'TCN',
 'OPCVM_ACTION',
 'OPCVM_Obligataire',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Risque']


col_rc = [ 'Profil_Risque','Id_Personne']

col_ra = ['Risqué', 'Equilibré', 'Prudent','Année']

col_pr = ['Risqué', 'Equilibré', 'Prudent']

col_vq = [ 'Action_Non_Matérialisée',
 'Action_Matérialisée',
 'Obligation_Non_Matérialisée',
 'Obligation_Matérialisée',
 'Droit',
 'TCN',
 'OPCVM_ACTION',
 'OPCVM_Obligataire',
 'OPCVM_Monétaire',
 'OPCVM_Diversifiée_Action',
 'OPCVM_Diversifiée_Obligation',
 'BDP',
 'OR',
 'Total',
 'Type']

col_rv = ['Prudent', 'Equilibré', 'Risqué', 'Type']












