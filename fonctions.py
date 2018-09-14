# Functions ##########################################
import pandas as pd
import numpy as np

##########################################################################################################################################################

def index_to_question(indexes):
    #Takes a list of indexes and returns question labels for the very first part 
    L = []
    for index in indexes:
        L.append('Q'+str(index))
    return L

##########################################################################################################################################################
    
def label_to_index(df, labels):
    indexes = []
    for string in labels:
        index = df.columns.get_loc(string)
        indexes.append(index)
    return indexes

##########################################################################################################################################################

def del_columns(DataFrame, rate = 0.5 ):
    #Takes a dataframe and a the rate of missing values allowed in each column
    #Returns a Dataframe without the columns with more missing values
    df = DataFrame
    empty = pd.DataFrame(df.isnull().sum())
    threshold = len(df)*rate
    to_delete = [DataFrame.columns[i] for i in range(len(empty)) if empty[0][i]>threshold]
    df = df.drop(to_delete, axis = 1) 
    return df

##########################################################################################################################################################

def del_rows(DataFrame, rate = 0.5 ):
    #Takes a dataframe and a the rate of missing values allowed in each row
    #Returns a Dataframe without the rows with more missing values
    df = DataFrame
    empty = pd.DataFrame(df.T.isnull().sum())
    threshold = len(df.T)*rate
    to_delete = [i for i in range(len(empty)) if empty[0][i]>threshold]
    df = df.drop(to_delete) 
    return df

##########################################################################################################################################################

def categoriser(dataframe = pd.DataFrame([]), index = None, s = pd.Series([]), labels=None, no_drop = False):
    #takes s of type pd.Series which is a categorical numerised variable
    #Or take datafram with index to catch pd.Series
    #returns a DataFrame of binary vectors of the categories
    if not s.empty : 
        if no_drop : 
            data = pd.get_dummies(s)
        else :
            data = pd.get_dummies(np.where(s==s.unique()[0], None, s))
        if labels != None :
            labels = [labels[int(i)] for i in data.columns] # data.columns contains the column indexes (useful if no_drop=False)
            data.columns = labels
        return data
    
    if not dataframe.empty :
        df = categoriser(s = dataframe.iloc[:,index], labels = labels)
        frames = [dataframe.iloc[:,:index], df, dataframe.iloc[:,index+1:]]
        return pd.concat(frames, axis = 1)

##########################################################################################################################################################    

def summer(dataframe, columns = None, label = None):
    #Takes dataframe, columns, label
    if columns == None :
        return summer(dataframe, dataframe.columns, label)
    if label == None : 
        label = 'Somme des colonnes : '
        for col in columns: 
            label += str(col)
        return summer(dataframe, columns, label )
    else : 
        
        if not isinstance(columns[0],int):
            return summer(dataframe, label_to_index(dataframe, columns), label)
        else :
            first_index = columns[0]
            first_df = dataframe.iloc[:,:first_index]
            summed_df = pd.DataFrame(dataframe.iloc[:,columns].sum(axis = 1))
            summed_df.columns = [label]
            to_delete = [dataframe.columns[index] for index in columns]
            last_df = dataframe.iloc[:,first_index:].drop(to_delete, axis = 1)
            df = pd.concat([first_df,summed_df,last_df], axis=1)
            return df
            
# Scoring #########################################################################################################################################################


def scorer (df):

    #Connaissance du marché (questions : 1,2,3,4,5,7,9)
    df[['Q2','Q3','Q4','Q5','Q7']] = df[['Q2','Q3','Q4','Q5','Q7']].multiply(5, axis = 1) 
    df = summer(df, ['Q2','Q3','Q4','Q5','Q7'], label = 'instruments_connus')
    df[['Q9']] = df[['Q9']].multiply(10, axis = 1) 
    df = summer(df,['Q1','instruments_connus','Q9'], label = 'connaissance_marche')
    
    #Tolerance au risque (questions : 10,11,12,13,14,19,20,29
    df[index_to_question([10,14])] = df[index_to_question([10,14])].multiply(15, axis = 1) 
    df[index_to_question([11,12,13])] = df[index_to_question([11,12,13])].multiply(5, axis = 1) 
    df[index_to_question([29])] = df[index_to_question([29])].multiply(15, axis = 1) 
    df = summer(df,index_to_question([10,11,12,13,14,19,20,29]), label = 'tolerance_risque')
    
    #Situation patrimoniale (questions : 45 )
    df[index_to_question([45])] = df[index_to_question([45])].multiply(15, axis = 1) 
    df['situation_patrimoniale'] = df[index_to_question([45])]
    df = df.drop(index_to_question([45]), axis=1)
    
    #Horizon (questions : 26 )
    df['horizon'] = df[index_to_question([26])]
    df = df.drop(index_to_question([26]), axis=1)
    
    #Objectif d'investissement(questions : 21,22,23,24,32 )
    df[index_to_question([21])] = df[index_to_question([21])].multiply(15, axis = 1) 
    df[index_to_question([22])] = df[index_to_question([22])].multiply(10, axis = 1) 
    df[index_to_question([23])] = df[index_to_question([23])].multiply(5, axis = 1) 
    df[index_to_question([24])] = df[index_to_question([24])].multiply(20, axis = 1) 
    df = summer(df,index_to_question([21,22,23,24,32]), label = 'objectif_investissement')
    
    #Temps disponible (question : 30)
    df['temps_disponible'] = df[index_to_question([30])]
    df = df.drop(index_to_question([30]), axis=1)
    
    #Mode de gestion (question : 16,18)
    table = np.array(df[['Q16','Q18']].values).T
    scalar = table[0]*table[1]
    df = df.drop(['Q16','Q18'], axis=1)
    df['mode_gestion']=pd.DataFrame(scalar)
    
    return df

##########################################################################################################################################################    

def maxer(df, label = None):
    #returns the index of the maximum value in each row in a single column dataframe
    data = df
    length = len(df.iloc[:,[0]])
    for index in range(length) :
        row = df.iloc[index]
        maxi = max(row)
        column_index = row[row == maxi].index[0]
        data.iloc[index,[column_index]] = 1
        for i in range(4) :
            if i!=column_index :
                data.iloc[index,[i]] = 0
    return data



##########################################################################################################################################################    
#
#def labeller(df):
#    #Takes a matrix of zeros and ones and return the label of the first one in each row
#    length = len(df.iloc[:,[0]])
#    for index in range(length) :
#        row = df.iloc[index]
#        column_index = row[row == 1].index[]
#        
#    
    
    
    

##########################################################################################################################################################    


