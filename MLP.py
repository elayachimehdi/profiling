
#Importation des libraires
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#Importation du dataset 
from data_preparation import df as X
from data_preparation import output as y


# Séparation du training set et du test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

#Importing keras modules
from keras.models import Sequential 
from keras.layers import Dense, Dropout



#Initiation 
classifier = Sequential()

#Ajouter la  d'entrée
classifier.add(Dense(units=7, activation="relu", 
                     kernel_initializer="uniform", input_dim=7))
classifier.add(Dropout(rate=0.1))

#Ajouter une couche cachée
classifier.add(Dense(units=32, activation="relu", 
                     kernel_initializer="uniform"))
classifier.add(Dropout(rate=0.1))

#Ajouter une couche cachée
classifier.add(Dense(units=64, activation="relu", 
                     kernel_initializer="uniform"))
classifier.add(Dropout(rate=0.1))

#Ajouter une couche cachée
classifier.add(Dense(units=32, activation="relu", 
                     kernel_initializer="uniform"))
classifier.add(Dropout(rate=0.1))

#Ajouter la couche de sortie
classifier.add(Dense(units=4, activation="sigmoid", 
                     kernel_initializer="uniform"))

classifier.compile(optimizer="adam",loss="categorical_crossentropy", metrics=["accuracy"]) 
 #loss=categorical_crossentropy dans le cas de plusieur neurones de sortie
 
 
#Training Neural Network
classifier.fit(X_train,y_train, batch_size=10, epochs=100)

#Prediction 
from fonctions import maxer
y_pred = classifier.predict(X_test)
y_pred = maxer(pd.DataFrame(y_pred))

#Confusion Matrix 
from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(y_test.iloc[:,0], y_pred.iloc[:,0])



# Grid Search 
#Libraries
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

#Building Function
def build_classifier(optimizer):
    #Initiation 
    classifier = Sequential()
    
    classifier.add(Dense(units=7, activation="relu", 
                         kernel_initializer="uniform", input_dim=7))
    classifier.add(Dropout(rate=0.1))
    
    classifier.add(Dense(units=16, activation="relu", 
                         kernel_initializer="uniform"))
    classifier.add(Dropout(rate=0.1))
    
    classifier.add(Dense(units=32, activation="relu", 
                         kernel_initializer="uniform"))
    classifier.add(Dropout(rate=0.1))
    
    classifier.add(Dense(units=4, activation="sigmoid", 
                         kernel_initializer="uniform"))

    classifier.compile(optimizer=optimizer,loss="categorical_crossentropy", metrics=["accuracy"]) 
    
    return classifier



classifier = KerasClassifier(build_fn=build_classifier)
parameters = {"batch_size":[25,32],
              "epochs":[100,500],
              "optimizer":["adam","rmsprop"]}
grid_search = GridSearchCV(estimator = classifier, 
                           param_grid = parameters, 
                           scoring="accuracy", 
                           cv=10)

grid_search = grid_search.fit(X_train,y_train)
best_params = grid_search.best_params_
best_precision = grid_search.best_score_







































