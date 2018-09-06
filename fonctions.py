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

def categoriser(dataframe = pd.DataFrame([]), index = None, s = pd.Series([]), labels=None):
    #takes s of type pd.Series which is a categorical numerised variable
    #Or take datafram with index to catch pd.Series
    #returns a DataFrame of binary vectors of the categories
    if not s.empty : 
        data = pd.get_dummies(np.where(s==s.unique()[0], None, s))
        if labels != None :
            labels = [labels[int(i)] for i in data.columns]
            data.columns = labels
        return data
    
    if not dataframe.empty :
        df = categoriser(s = dataframe.iloc[:,index], labels = labels)
        frames = [dataframe.iloc[:,:index], df, dataframe.iloc[:,index+1:]]
        return pd.concat(frames, axis = 1)

##########################################################################################################################################################    

def summer(dataframe, columns, label = None):
    #Takes dataframe, columns, label
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
            
##########################################################################################################################################################












