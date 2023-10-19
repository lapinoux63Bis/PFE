
import pandas as pd
import os


##

##

data2 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\HUMIDITE", names = ["Temps","Humdity"])
print(data2)

##

data3 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\registre_transmissions.csv",delimiter = ';', names = ["Temps","Ip_src", "Ip_dest","Port_src","Port_dest","sup1","sup2","protocole"])
data3 = data3.drop(["sup1", "sup2"], axis=1)
print(data3)

##
data4 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TEMPERATURE", names = ["Temps","Temperature"])
print(data4)

##

data5 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\LUMINOSITE", names = ["Temps","Luminosity"])
print(data5)


##

data6 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TCPU\TCPU1", names = ["Temps","Tcpu1"])
print(data6)

##

data7 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque2_scanning\TCPU\TCPU2", names = ["Temps","Tcpu2"])
print(data7)

##

data8 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1\FCPU\FCPU1", names = ["Temps","Fcpu1"])
print(data8)

##

data9 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque2_scanning\FCPU\FCPU2", names = ["Temps","Fcpu2"])
print(data9)

##

data10 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1\DELAY", names = ["Temps","Delay"])
print(data10)

##

data11 = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\BOUTON", names = ["Temps","Bouton"])
print(data11)

##
def ajouter_noms_de_colonnes(fichier_entree, noms_colonnes):
    """
    Ajoute des noms de colonnes à un fichier CSV.

    Args:
        fichier_entree (str): Le nom du fichier CSV d'entrée.
        fichier_sortie (str): Le nom du fichier CSV de sortie avec les noms de colonnes ajoutés.
        noms_colonnes (list): Une liste de noms de colonnes à ajouter.

    Returns:
        None
    """
    # Chargez le fichier CSV d'entrée
    df = pd.read_csv(fichier_entree)

    # Vérifiez que le nombre de noms de colonnes correspond au nombre de colonnes dans le fichier
    if len(noms_colonnes) != len(df.columns):
        print("Le nombre de noms de colonnes ne correspond pas au nombre de colonnes dans le fichier.")
        return

    # Attribuez les noms de colonnes au DataFrame
    df.columns = noms_colonnes

    # Enregistrez le DataFrame avec les noms de colonnes dans un nouveau fichier CSV
    df.to_csv(fichier_entree+".csv", index=False)
##

def ajouter2(attaque):
    chemin_base = r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS"
    attaque_path = os.path.join(chemin_base, attaque)
    ajouter_noms_de_colonnes(attaque_path +"\TCPU1",["Temps","Tcpu1"])
    ajouter_noms_de_colonnes(attaque_path+"\TCPU2",["Temps","Tcpu2"])
    ajouter_noms_de_colonnes(attaque_path+"\FCPU2",["Temps","Fcpu2"])
    ajouter_noms_de_colonnes(attaque_path+"\FCPU1",["Temps","Fcpu1"])
    ajouter_noms_de_colonnes(attaque_path+"\TEMPERATURE",["Temps","Temperature"])
    ajouter_noms_de_colonnes(attaque_path+"\LUMINOSITE",["Temps","Luminosite"])
    ajouter_noms_de_colonnes(attaque_path+"\HUMIDITE",["Temps","Humidite"])
    ajouter_noms_de_colonnes(attaque_path+"\DELAY",["Temps","Delay"])


##

def convertir_temperature_en_celsius(fichier_entree, colonne):
    """
    Convertit les températures en degrés Celsius dans un fichier CSV.

    Args:
        fichier_entree (str): Le nom du fichier CSV d'entrée.
        fichier_sortie (str): Le nom du fichier CSV de sortie avec les températures en °C.

    Returns:
        None
    """
    # Chargez le fichier CSV d'entrée
    df = pd.read_csv(fichier_entree)

    # Vérifiez si le fichier contient une colonne "Temperature" en °F
    if colonne in df.columns:
        # Convertissez les températures en degrés Celsius
        df[colonne] = (df[colonne] - 32) / 1.8

        # Enregistrez le DataFrame avec les températures converties en degrés Celsius dans un nouveau fichier CSV
        df.to_csv(fichier_entree, index=False)

##

def convert2(attaque):
    chemin_base = r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI"
    attaque_path = os.path.join(chemin_base, attaque)
    convertir_temperature_en_celsius(attaque_path +"\TCPU1.csv", "Tcpu1")
    convertir_temperature_en_celsius(attaque_path +"\TCPU2.csv", "Tcpu2")

##
##

def ajouter3(attaque):
    chemin_base = r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS"
    attaque_path = os.path.join(chemin_base, attaque)
    data1 = pd.read_csv(attaque_path + "\cpu_stats.csv",names=["Temps", "Temperature", "Frequency", "Cpu_usage", "Cpu_memory"],
    delimiter=";")
    data1.to_csv(attaque_path + "\cpu_stats.csv", index=False)



##
"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\SSH_bruteforce_test_2\cpu_stats.csv"

##

def ajouterclasse(chemin, temps,type_attaque):
    data = pd.read_csv(chemin,
    delimiter=",")
    data["Classe"]= "normal"
    n = len(temps)
    m =len(data)
    i = 0
    while i < n:
        for j in range(0,m):
            if temps[i+1] >= data.at[j,"Temps"] >= temps[i]:
                data.at[j,"Classe"] = type_attaque
        i = i + 2
    data.to_csv(chemin, index= False)

##

ajouterclasse(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\SSH_bruteforce_test_2\cpu_stats.csv",[1697197378,1697198562,1697200473,1697202754,1697204715,1697206347], "SSH_bruteforce")

##

ajouterclasse(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\MQTT_bruteforce2\cpu_stats.csv",[1697227843,1697228368,1697229066,1697229641,1697230306,1697230744,1697231415,1697231827], "MQTT_bruteforce")






    ##

a = r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\SSH_bruteforce_test_2\cpu_stats.csv"



##

ajouterclasse(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\DoS_attack1\cpu_stats.csv",[1697490636,1697491577,1697492255,1697493129,1697493825,1697494584], "DoS_attack")



##

a = pd.read_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\cpu_stats.csv", names = ["Temps", "Temperature", "Frequency", "Cpu_usage", "Cpu_memory"],delimiter=";")

a.to_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\cpu_stats.csv", index= False)






