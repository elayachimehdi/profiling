#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									K MEANS CLUSTERING
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

# K means clustering is applied to normalized ipl player data


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd 
from mpl_toolkits.mplot3d import Axes3D

style.use('ggplot')

class K_Means:
	def __init__(self, k =3, tolerance = 0.0001, max_iterations = 500):
		self.k = k
		self.tolerance = tolerance
		self.max_iterations = max_iterations

	def fit(self, data):

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
			for features in data:
				distances = [np.linalg.norm(features - self.centroids[centroid]) for centroid in self.centroids]
				classification = distances.index(min(distances))
				self.classes[classification].append(features)

			previous = dict(self.centroids)

			#average the cluster datapoints to re-calculate the centroids
			for classification in self.classes:
				self.centroids[classification] = np.average(self.classes[classification], axis = 0)

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
    index = 0
    df = pd.read_csv(r"./score_standardise.csv").drop(['Unnamed: 0'], axis = 1)
    X = df.values #returns a numpy array
    km = K_Means(4)
    km.fit(X)

    # Plotting starts here
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    colors = ["r", "g", "c", "b", "k"]

    for centroid in km.centroids:
        ax.scatter(km.centroids[centroid][0], km.centroids[centroid][1],km.centroids[centroid][2], s = 130, marker = "x")

    for classification in km.classes:
        color = colors[classification]
        Dataframe[str(index)] = pd.Series(km.classes[classification])
        for features in km.classes[classification]:
            ax.scatter(features[0], features[1], features[2], color = color,s = 30)
	
    plt.show()
    return Dataframe

    

if __name__ == "__main__":
	main()    
    

    
    
    
    
    
    
    
    
    
    