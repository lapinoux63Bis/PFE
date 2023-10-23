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
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz/bin/'





## DATAS BRUTE FORCE

# Charger vos données depuis un fichier CSV

#registre trans
data_attaque_trans = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\registre_transmissions.csv",delimiter = ';', names = ["Temps","Ip_src", "Ip_dest","Port_src","Port_dest","sup1","sup2","protocole"]) #delimiter seulement pour registre_transmissions

data_attaque_trans = data_attaque_trans.drop(["sup1", "sup2"], axis=1) #que pour registre-transmissions

data_sain_trans = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\registre_transmissions.csv",delimiter = ';', names = ["Temps","Ip_src", "Ip_dest","Port_src","Port_dest","sup1","sup2","protocole"]) #chemin d'acces a modifier
data_sain_trans = data_sain_trans.drop(["sup1", "sup2"], axis=1)

#cpu_usage

data_sain_cpuusage = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\cpu_stats.csv", names = ["Temps","Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])

data_attaque_cpuusage = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\cpu_stats.csv", names = ["Temps","Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])

#fcpu

data_sain_fcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\FCPU\FCPU1", names = ["Temps","Fcpu1"])

data_sain_fcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\FCPU\FCPU2", names = ["Temps","Fcpu2"])


data_attaque_fcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\FCPU\FCPU1", names = ["Temps","Fcpu1"])

data_attaque_fcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\FCPU\FCPU2", names = ["Temps","Fcpu2"])

#tcpu

data_sain_tcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TCPU\TCPU1", names = ["Temps","Tcpu1"])

data_sain_tcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TCPU\TCPU2", names = ["Temps","Tcpu2"])


data_attaque_tcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\TCPU\TCPU1", names = ["Temps","Tcpu1"])

data_attaque_tcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\TCPU\TCPU2", names = ["Temps","Tcpu2"])


#delay

data_sain_delay = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\DELAY", names = ["Temps","Delay"])

data_attaque_delay = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\DELAY", names = ["Temps","Delay"])

#TEMPERATURE

data_sain_temperature = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TEMPERATURE", names = ["Temps","Temperature"])

data_attaque_temperature = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\TEMPERATURE", names = ["Temps","Temperature"])

#Luminosity

data_sain_luminosity = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\LUMINOSITE", names = ["Temps","Luminosity"])

data_attaque_luminosity = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforcemqtt\LUMINOSITE", names = ["Temps","Luminosity"])


#temps

temps_debut_attaque = 1697016963
temps_fin_attaque = 1697017272

temps_debut_attaque13 = 1697016963000
temps_fin_attaque13 = 1697017272000


## auxiliary function

def labell_temps(d,temps_fin,temps_debut,type_attaque):
    for i in range(1, len(d)):
        if temps_fin >= d.at[i,"Temps"] >= temps_debut:
            d.at[i,"Classe"] = type_attaque

## TRAIN

def classer(data_attaque1, data_sain1,temps_fin,temps_debut):
    data_attaque1["Classe"] = "normal"
    data_sain1["Classe"] = "normal"
    labell_temps(data_attaque1,temps_fin,temps_debut,"bruteforcemqtt")
    datatrain = pd.concat([data_sain1, data_attaque1], ignore_index=True)
    datatrain = datatrain.drop(['Temps'], axis= 1)
    return datatrain


def encodage(datatrain):
    label_encoder = LabelEncoder()
    datatrain['Ip_src'] =  label_encoder.fit_transform(datatrain['Ip_src'])
    datatrain["Ip_dest"] = label_encoder.fit_transform(datatrain["Ip_dest"])
    datatrain["Port_src"] = label_encoder.fit_transform(datatrain["Port_src"])
    datatrain["Port_dest"] = label_encoder.fit_transform(datatrain["Port_dest"])
    datatrain["protocole"] = label_encoder.fit_transform(datatrain["protocole"])



def apprentissage(datatrain):
    y = datatrain["Classe"]
    x = datatrain.drop("Classe", axis = 1)
    modele_rf = RandomForestClassifier(
        n_estimators=100,
        criterion='gini',
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features=None,)
    modele_rf.fit(x, y)
    pd.DataFrame(modele_rf.feature_importances_,
                index = x.columns,
                columns = ["importance"]).sort_values(
        "importance",
        ascending = False)

    importances = list(modele_rf.feature_importances_)
    feature_list = list(x.columns)

    # list of x locations for plotting
    x_values = list(range(len(importances)))# Make a bar chart
    plt.bar(x_values, importances, orientation = 'vertical', color = 'r',                       edgecolor = 'k', linewidth = 1.2)# Tick labels for x axis
    plt.xticks(x_values, feature_list, rotation='vertical')# Axis labels    and title
    plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable   Importances');
    plt.show()

## création des datatrains

datatrain_cpuusage = classer(data_attaque_cpuusage,data_sain_cpuusage,temps_fin_attaque,temps_debut_attaque)
datatrain_delay = classer(data_attaque_delay,data_sain_delay,temps_fin_attaque13,temps_debut_attaque13)
datatrain_trans = classer(data_attaque_trans,data_sain_trans,temps_fin_attaque,temps_debut_attaque)
datatrain_tcpu1 = classer(data_attaque_tcpu1,data_sain_tcpu1,temps_fin_attaque,temps_debut_attaque)
datatrain_tcpu2 = classer(data_attaque_tcpu2,data_sain_tcpu2,temps_fin_attaque,temps_debut_attaque)
encodage(datatrain_trans)
## apprentissage


apprentissage(datatrain_cpuusage)

apprentissage(datatrain_delay)

apprentissage(datatrain_trans)
apprentissage(datatrain_tcpu1)
apprentissage(datatrain_tcpu2)

## DATAS TEST

# Charger vos données depuis un fichier CSV

#registre trans
data_test_trans = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\registre_transmissions.csv",delimiter = ';', names = ["Temps","Ip_src", "Ip_dest","Port_src","Port_dest","sup1","sup2","protocole"]) #delimiter seulement pour registre_transmissions

data_test_trans = data_test_trans.drop(["sup1", "sup2"], axis=1) #que pour registre-transmissions

encodage(data_test_trans)

#cpu_usage

data_test_cpuusage = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\cpu_stats.csv", names = ["Temps","Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])


#fcpu

data_test_fcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\FCPU\FCPU1", names = ["Temps","Fcpu1"])

data_test_fcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\FCPU\FCPU2", names = ["Temps","Fcpu2"])


#tcpu

data_test_tcpu1 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\TCPU\TCPU1", names = ["Temps","Tcpu1"])

data_test_tcpu2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\TCPU\TCPU2", names = ["Temps","Tcpu2"])


#delay

data_test_delay = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\DELAY", names = ["Temps","Delay"])


#Temperature

data_test_temperature = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\TEMPERATURE", names = ["Temps","Temperature"])


#Luminosity

data_test_luminosity = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\test1_bruteforcemqtt\LUMINOSITE", names = ["Temps","Luminosity"])

#TEMPS
temps_debut_test = 1697017574
temps_fin_test= 1697017655

temps_debut_test13 = 1697017574000
temps_fin_test13 = 1697017655000





##
# Initialiser une colonne "Anomalie" avec des valeurs par défaut à "Non"
def classer2(datatest,temps_fin,temps_debut):
    datatest["Classe"] = "normal"
    labell_temps(datatest,temps_fin,temps_debut,"bruteforcemqtt")
    datatest = datatest.drop(['Temps'], axis= 1)
    return datatest

##classer datatest

## création des datatrains

data_test_cpuusage = classer2(data_test_cpuusage,temps_fin_test,temps_debut_test)
data_test_delay = classer2(data_test_delay,temps_fin_test13,temps_debut_test13)
data_test_trans = classer2(data_test_trans,temps_fin_test,temps_debut_test)
data_test_tcpu1 = classer2(data_test_tcpu1,temps_fin_test,temps_debut_test)
encodage(data_test_trans)
data_test_tcpu2 = classer2(data_test_tcpu2,temps_fin_test,temps_debut_test)


## test
def test(datatest,datatrain):
    y = datatrain["Classe"]
    x = datatrain.drop("Classe", axis = 1)
    modele_rf = RandomForestClassifier(
        n_estimators=200,
        criterion='gini',
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features=None,)
    modele_rf.fit(x, y)
    pd.DataFrame(modele_rf.feature_importances_,
                index = x.columns,
                columns = ["importance"]).sort_values(
        "importance",
        ascending = False)

    importances = list(modele_rf.feature_importances_)
    feature_list = list(x.columns)
    xt = datatest.drop("Classe", axis = 1)
    yt = datatest["Classe"]
    modele_rf.predict(xt)
    print(f"The percentage of correctly classified is : {accuracy_score(yt, modele_rf.predict(xt))*100} %")


    print(pd.DataFrame(confusion_matrix(yt, modele_rf.predict(xt)),
                index = ["attaque_donnés", "safe_données"],
                columns = ["attaque_predit", "safe_predit"]))

    conf_matrix = confusion_matrix(yt, modele_rf.predict(xt))
    tn, fp, fn, tp = conf_matrix.ravel()
    # Calcul du total
    total = tp + tn + fp + fn
    # Calcul des pourcentages
    tp_percentage = (tp / total) * 100
    tn_percentage = (tn / total) * 100
    fp_percentage = (fp / total) * 100
    fn_percentage = (fn / total) * 100

    # Affiche les pourcentages
    print(f"True Positives (TP): {tp_percentage:.2f}%")
    print(f"True Negatives (TN): {tn_percentage:.2f}%")
    print(f"False Positives (FP): {fp_percentage:.2f}%")
    print(f"False Negatives (FN): {fn_percentage:.2f}%")




## find best parameters

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50,100, 200, 300],
    'max_depth': [None, 5, 10, 20,20,40,50],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(x, y)
best_params = grid_search.best_params_
##
test(data_test_cpuusage,datatrain_cpuusage)


##

test(data_test_trans,datatrain_trans)


##

test(data_test_delay, datatrain_delay)
##

test(data_test_tcpu1, datatrain_tcpu1)

##


test(data_test_tcpu2, datatrain_tcpu2)


##
test2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\cpu_stats.csv", names = ["Temps","Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])
test2["Classe"] = "normal"
test2 = test2.drop("Temps", axis = 1)


##

test(test2, datatrain_cpuusage)
