#================================================================================================================#
#----------------------------------------------------------------------------------------------------------------#
#									K MEANS CLUSTERING                                                           #
#----------------------------------------------------------------------------------------------------------------#
#================================================================================================================#

# K means clustering is applied to normalized ipl player data &

import pyodbc as db
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd 
from mpl_toolkits.mplot3d import Axes3D
from fonctions import classifier

style.use('ggplot')
score_columns = ['connaissance_marche',
 'tolerance_risque',
 'objectif_investissement',
 'situation_patrimoniale',
 'horizon',
 'temps_disponible',
 'mode_gestion']


class K_Means:
    def __init__(self, k =3, tolerance = 0.0001, max_iterations = 500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations


    def fit(self, df):
        labels = df.index
        data = df.values
        self.centroids = {}
        #initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        for i in range(self.k):
            self.centroids[i] = data[i]

        #begin iterations
        for i in range(self.max_iterations):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            #find the distance between the point and cluster; choose the nearest centroid
            label = -1
            for features in data:
                label +=1
                distances = [np.linalg.norm(features - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classes[classification].append(np.concatenate((features,np.array([labels[label]]))))
                
            previous = dict(self.centroids)

            #average the cluster datapoints to re-calculate the centroids
            for classification in self.classes:
                self.centroids[classification] = np.average(self.classes[classification], axis = 0)[:len(data[0])]
            isOptimal = True

            for centroid in self.centroids:

                original_centroid = previous[centroid]
                curr = self.centroids[centroid]
                
                
                
                if np.sum((curr - original_centroid)/original_centroid * 100.0) > self.tolerance:
                    isOptimal = False

            #break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
            if isOptimal:
                break


    def pred(self, data):
        distances = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification




def main():
    Dataframe = pd.DataFrame()
    df = pd.read_csv(r"./Data_before_clustering.csv")
    df.index = df['IdPersonne']
    df = df.drop('IdPersonne',axis = 1)
    
    
    km = K_Means(4)
    km.fit(df)

    # Plotting starts here
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    colors = ["r", "g", "c", "b", "k"]

    for centroid in km.centroids:
        ax.scatter(km.centroids[centroid][0], km.centroids[centroid][1],km.centroids[centroid][2], s = 130, marker = "x")

    for classification in km.classes:
        color = colors[classification]
        class_output = pd.concat([pd.DataFrame(km.classes[classification]),pd.DataFrame(np.ones(len(km.classes[classification]))*classification)],axis = 1)
        if Dataframe.empty : 
            Dataframe = class_output
        else : 
            Dataframe = pd.concat([Dataframe,class_output],axis = 0)
            
        for features in km.classes[classification]:
            ax.scatter(features[0], features[1], features[2], color = color,s = 30)
    plt.show()
    Dataframe.columns = score_columns + ['IdPersonne','classe']
    con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=ZBOOK;Trusted_Connection=yes;DATABASE=Peaqock')
    quest = pd.read_sql('SELECT * FROM Peaqock.dbo.KYC',con)
    Dataframe['Score_total'] = Dataframe[score_columns].sum(axis = 1)    
    Dataframe['Score_classe'] = classifier(Dataframe['Score_total'],limits = [-1.5,0.5,4])
    Dataframe = pd.merge(Dataframe, quest, left_on = 'IdPersonne', right_on = 'IdPersonne' )
    
    return Dataframe



if __name__ == "__main__":
	main()

















