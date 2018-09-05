# Functions ##########################################
import pandas as pd
import numpy as np

def index_to_question(indexes):
    #Takes a list of indexes and returns question labels
    L = []
    for index in indexes:
        L.append('Q'+str(index+1))
    return L


def del_columns(DataFrame, rate = 0.5 ):
    #Takes a dataframe and a the rate of missing values allowed in each column
    #Returns a Dataframe without the columns with more missing values
    df = DataFrame
    empty = pd.DataFrame(df.isnull().sum())
    threshold = len(df)*rate
    to_delete = [i for i in range(len(empty)) if empty[0][i]>threshold]
    df = df.drop(index_to_question(to_delete), axis = 1) 
    return df


def del_rows(DataFrame, rate = 0.5 ):
    #Takes a dataframe and a the rate of missing values allowed in each row
    #Returns a Dataframe without the rows with more missing values
    df = DataFrame
    empty = pd.DataFrame(df.T.isnull().sum())
    threshold = len(df.T)*rate
    to_delete = [i for i in range(len(empty)) if empty[0][i]>threshold]
    df = df.drop(to_delete) 
    return df

def categoriser(dataframe = pd.DataFrame([]), index = None, s = pd.Series([]), labels=None):
    #takes s of type pd.Series which is a categorical numerised variable
    #returns a DataFrame of binary vectors of the categories
    if not s.empty : 
        data = pd.get_dummies(np.where(s==s.unique()[0], None, s))
        if labels != None :
            print('columns :', data.columns)
            labels = [labels[int(i)] for i in data.columns]
            data.columns = labels
        return data
    if not dataframe.empty :
        df = categoriser(s = dataframe.iloc[:,index], labels = labels)
        frames = [dataframe.iloc[:,:index], df, dataframe.iloc[:,index+1:]]
        return pd.concat(frames, axis = 1)
    

