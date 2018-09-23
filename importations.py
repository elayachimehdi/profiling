import pyodbc as db  
import pandas as pd 



con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
cur = con.cursor()
df = pd.read_sql("""SELECT * 
  FROM (((peaqock.dbo.TransactionsHist
  inner join Peaqock.dbo.OrdresHist  ON  Peaqock.dbo.TransactionsHist.IdOrdreEx = Peaqock.dbo.OrdresHist.IdOrdreEx)
      INNER join peaqock.dbo.ComptesEspece ON IdCompte=IdCompteEspece)
          INNER join Peaqock.dbo.Clients  ON IdClient=IdPersonne)""",con)



df.index = df['IdPersonne']
df = pd.DataFrame(df)
Id_Personne_KYC = list(set(pd.read_sql("SELECT IdPersonne FROM KYC",con)['IdPersonne']))
df = df.loc[Id_Personne_KYC]





#
#def table_commander(table_name, column_names, row_example):
#    sql_types = ['CHARACTER',]
#    python_type = [ ]
#    column_types = []
#    if len(column_names)!=len(row_example):
#        print("lenght of names : ", len(column_names))
#        print("length of example : ", len(row_example))
#    length = len(column_example)
#    command = 'CREATE TABLE IF NOT EXISTS' + table_name + ' ('
#    for name in column_names : 
#        command += 
#    

def execom(command, con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')):
    cur = con.cursor()
    cur.execute(command)
    cur.close()
    
    

    
    
    
def insert(table_name, df, column_names):
    
    command = 'INSERT INTO '+table_name+' ('
    for column_name in column_names : 
        command += column_name + ','
    command = command[:-1]
    command += ') VALUES '
    for row in df.index : 
        command += str(tuple(df.loc[row]))+','
    command = command[:-1]
    return command

















con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
execom('CREATE TABLE Testing1')













