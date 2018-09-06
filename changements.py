#Changements
''' Pour ajouter une liste, il faut : 
    +++ ajouter les listes old et new parmi les listes de chagements
    +++ ajouter le nom de la liste new dans la liste concaténée new 
    +++ ajouter le nom de la liste old dans la liste concaténée old
'''

#Listes des changements #################################################################################################################################################################

ouinon = ['Oui','Oui ', 'Non']
unzero = [1,1,0]

Q1_old = ['Exige un accompagnement en la matière','Modérée','Moyenne','Excellente']
Q1_new = [5,10,15,20]

Q18_old = ['Jamais','Rarement','Régulièrement']
Q18_new = [5,10,15]

Q19_old = ['Jamais ','Jusqu’à 1 an','1-5 ans','Plus de 5 ans']
Q19_new = [0,5,10,15]

Q20_old = ['Aucune ','Jusqu’à 15','+ de 15']
Q20_new = [0,5,15]

Q26_old = ['Moins d’un an','Entre 1 et 3 ans','Entre 3 et 5 ans','Plus de à 5 ans']
Q26_new = [5,10,15,20]

Q28_old = ['Prudent','Equilibré', 'Dynamique','Offensif']
Q28_new = [0,1,2,3]

Q30_old = ['En une fois',' Selon les opportunités du marché','En plusieurs interventions périodiques ']
Q30_new = [5,10,15]

Q32_old = ['Une prise de bénéfices ferme ;','Un réinvestissement des profits réalisés sur le marché','Une orientation des profits vers d’autres placements ']
Q32_new = [5,15,10]

#Ces varibles ne sont pas ordonnées 
Q36_old = ['Cadre','Profession libérale','Sans profession','Retraité','Artisan','Chef d’entreprise','Enseignant','Fonctionnaire','Employé','Etudiant','Expert banque et finances','Commerçant']
Q36_new = [0,1,2,3,4,5,6,7,8,9,10,11]

Q45_old = ['Salaire','Rentes','Revenus immobiliers','Héritage','Retraite','Pension alimentaire']
Q45_new = [5,10,15,5,5,5]





#Listes concaténées #####################################################################################################################################################################
OLD = ouinon+Q1_old+Q18_old+Q19_old+Q20_old+Q26_old+Q28_old+Q30_old+Q32_old+Q36_old+Q45_old
NEW = unzero+Q1_new+Q18_new+Q19_new+Q20_new+Q26_new+Q28_new+Q30_new+Q32_new+Q36_new+Q45_new














