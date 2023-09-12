##Import

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import subprocess
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from os import system
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz/bin/'

##creation dataset
datatrain= pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\test arbre de decision\arff to csv\KDDTrain+.csv") #chemin d'accès à modifier


datatrain.head

##

datatrain["Classe"].value_counts()

##
datatrain.info()


## mise en forme du dataframe

datatrain = datatrain.drop(['duration','protocol_type','service','flag'], axis= 'columns')

##APPRENTISSAGE TEST
y = datatrain["Classe"]
x = datatrain.drop("Classe", axis = 1)


## Apprentissage de la forêt aléatoire


modele_rf = RandomForestClassifier(
     n_estimators=50,
     criterion='gini',
     max_depth=None,
     min_samples_split=2,
     min_samples_leaf=1,
     min_weight_fraction_leaf=0.0,
     max_features=6, #par défaut racine carré du nb de colonnes
     max_leaf_nodes=None,
     min_impurity_decrease=0.0,
     bootstrap=True,
     oob_score=False,
     n_jobs=None,
     random_state=None,
     verbose=0,
     warm_start=False,
     class_weight=None,
     ccp_alpha=0.0,
     max_samples=None,)


modele_rf.fit(x, y)


##

pd.DataFrame(modele_rf.feature_importances_,
              index = x_train.columns,
              columns = ["importance"]).sort_values(
     "importance",
     ascending = False)



##TEST

datatest=pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\test arbre de decision\arff to csv\KDDTest+.csv") #chemin d'accès à modifier

datatest.columns

datatest = datatest.drop(['duration','protocol_type','service','flag'], axis= 'columns')
xt = datatest.drop("Classe", axis = 1)
yt = datatest["Classe"]
##

modele_rf.predict(xt)

##

from sklearn.metrics import accuracy_score, confusion_matrix
print(f"Le pourcentage de bien classés est de : {accuracy_score(yt, modele_rf.predict(xt))*100} %")

##



pd.DataFrame(confusion_matrix(yt, modele_rf.predict(xt)),
             index = ["safe_donnés", "attaque_données"],
             columns = ["safe_predit", "attaque_predit"])




