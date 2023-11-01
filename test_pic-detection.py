import csv

##

##

nom_fichier_csv = pd.read_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\cpu_stats2.csv")

##
def detecter_anomalies(data_memory,data_usage,data_temperature,seuil, m, maxi,count):
    anomalies_usage = []  # Liste pour stocker les indices des anomalies
    fausses_anomalies_usage = []  # Liste pour stocker les indices des fausses anomalies
    anomalies_memory = []  # Liste pour stocker les indices des anomalies
    fausses_anomalies_memory = []  # Liste pour stocker les indices des fausses anomalies
    anomalies_temperature = []  # Liste pour stocker les indices des anomalies
    fausses_anomalies_temperature = []  # Liste pour stocker les indices des fausses anomalies
    anomalies_moyenne = []  # Liste pour stocker les indices des anomalies
    fausses_anomalies_moyenne = []  # Liste pour stocker les indices des fausses anomalies
    indice_usage = count - m[0]
    indice_memory = count - m[1]
    indice_temperature = count - m[2]
    indice_moyenne = count - m[3]
    valeur_usage = data_usage[indice_usage]
    valeur_memory = data_memory[indice_memory]
    valeur_temperature = data_temperature[indice_temperature]
    valeur_moyenne = sum(data_usage[indice_moyenne:indice_moyenne+m[3]])/m[3]
    if valeur_memory >=  maxi[1] + seuil[1]:
        suivantes = data_memory[indice_memory+1:indice_memory+m[1]+1]
        count2 = sum(1 for suivante in suivantes if suivante >= maxi[1] + seuil[1])
        if count2 <= 10:
            fausses_anomalies_memory.append(indice_memory)
            #maxi = max(maxi, valeur_actuelle)
        else:
            suivantes = data_usage[indice_usage:indice_usage + m[0]]
            count2 = sum(1 for suivante in suivantes if suivante >= maxi[0] + seuil[0])
            if count2 > 2:
                anomalies_usage.append(indice_usage)
            else:
                anomalies_memory.append(indice_memory)
    else:
        #print(valeur_moyenne)
        if valeur_moyenne >= maxi[3] + seuil[3]:
             anomalies_moyenne.append(indice_moyenne)
        #else:
            #maxi[3]=valeur_moyenne
    anomalies = [anomalies_usage, anomalies_memory, anomalies_temperature,anomalies_moyenne]
    fausses_anomalies = [fausses_anomalies_usage, fausses_anomalies_memory, fausses_anomalies_temperature,fausses_anomalies_moyenne]

    return anomalies, fausses_anomalies, maxi


##

def detect(dataset):
    data_memory = dataset["Cpu_memory"]
    data_usage = dataset["Cpu_usage"]
    data_temperature = dataset["Temperature"]
    tolerance_usage = 1
    tolerance_memory = 0.1
    tolerance_temperature = 2
    tolerance_moyenne = 1
    tolerance = [tolerance_usage,tolerance_memory,tolerance_temperature,tolerance_moyenne]
    maxi_memory = max(data_memory[50:100])
    maxi_usage = max(data_usage[50:100])
    maxi_temperature = max(data_temperature[50:100])
    moyenne = sum(data_usage[50:150])/100
    maxi = [maxi_usage,maxi_memory,maxi_temperature,moyenne]
    m = [50,50,50,50]
    anomalies, fausses_anomalies = [[],[],[],[]],[[],[],[],[]]
    print(moyenne)
    for i in range(100, len(data_memory)):
        new_anomalies, new_fausses_anomalies, new_maxi = detecter_anomalies(data_memory,data_usage,data_temperature,tolerance, m, maxi,i)
        anomalies[0] = anomalies[0]+(new_anomalies[0])
        anomalies[1] = anomalies[1]+(new_anomalies[1])
        anomalies[2] = anomalies[2]+(new_anomalies[2])
        anomalies[3] = anomalies[3]+(new_anomalies[3])
        fausses_anomalies[0] = fausses_anomalies[0]+(new_fausses_anomalies[0])
        fausses_anomalies[1] = fausses_anomalies[1]+(new_fausses_anomalies[1])
        fausses_anomalies[2] = fausses_anomalies[2]+(new_fausses_anomalies[2])
        fausses_anomalies[3] = fausses_anomalies[3]+(new_fausses_anomalies[3])
        maxi = new_maxi
    #print(anomalies,fausses_anomalies,maxi)
    dataset['Classe']= 'normal'

    for i in anomalies[0]:
        dataset.at[i, 'Classe'] = 'DoS'

    for i in anomalies[1]:
        dataset.at[i, 'Classe'] = 'SSH_bruteforce'

    for i in anomalies[3]:
        dataset.at[i, 'Classe'] = 'MQTT_bruteforce'
        dataset.to_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\cpu_stats_predict4.csv", index= False)


    # Nom du fichier texte
    nom_fichier_txt = "anomalies.txt"

    # Ouvrir le fichier texte en mode écriture
    with open(nom_fichier_txt, 'w') as fichier_txt:
        fichier_txt.write("Indices d'anomalies_usage: " + str(anomalies[0]) + "\n")
        fichier_txt.write("Indices d'anomalies_memory: " + str(anomalies[1]) + "\n")
        fichier_txt.write("Indices d'anomalies_moyenne: " + str(anomalies[3]) + "\n")

    # Création des sous-plots pour les graphiques d'anomalies
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Affichage du graphique des données brutes en nuage de points
    axes[0].scatter(range(0, len(data_usage)), data_usage[0:], c='b', label='Raw Data', s=5)
    axes[0].scatter(fausses_anomalies[0], [data_usage[i] for i in fausses_anomalies[0]], c='g', label='False Anomalies', s=10)
    axes[0].scatter(anomalies[0], [data_usage[i] for i in anomalies[0]], c='c', label='Anomalies usage', s=10)
    axes[0].set_title('Raw Data, Anomalies, and False Anomalies in CPU Usage')
    axes[0].set_xlabel('Index')
    axes[0].set_ylabel('CPU usage %')
    axes[0].legend()

    # Affichage du graphique des données brutes en nuage de points
    axes[1].scatter(range(0, len(data_memory)), data_memory[0:], c='b', label='Raw Data', s=5)
    axes[1].scatter(fausses_anomalies[1], [data_memory[i] for i in fausses_anomalies[1]], c='g', label='False Anomalies', s=10)
    axes[1].scatter(anomalies[1], [data_memory[i] for i in anomalies[1]], c='y', label='Anomalies memory', s=10)
    axes[1].set_title('Raw Data, Anomalies, and False Anomalies in Memory Usage')
    axes[1].set_xlabel('Index')
    axes[1].set_ylabel('Memory\'s usage of CPU %')
    axes[1].legend()

    # Affichage du graphique des données brutes en nuage de points
    axes[2].scatter(range(0, len(data_usage)), data_usage[0:], c='b', label='Raw Data', s=5)
    axes[2].scatter(fausses_anomalies[3], [data_usage[i] for i in fausses_anomalies[3]], c='g', label='False Anomalies', s=10)
    axes[2].scatter(anomalies[3], [data_usage[i] for i in anomalies[3]], c='m', label='Anomalies usage average', s=10)
    axes[2].set_title('Raw Data, Anomalies, and False Anomalies in CPU Usage average ')
    axes[2].set_xlabel('Index')
    axes[2].set_ylabel('CPU\'s usage average %')
    axes[2].legend()
    # Affichage des graphiques
    plt.tight_layout()
    plt.show()



