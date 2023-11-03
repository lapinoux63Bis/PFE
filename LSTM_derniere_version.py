import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

## importation

df_train = pd.read_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\cpu_stats2_true4.csv")
df_test = pd.read_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\SSH_bruteforce_3\cpu_stats2.csv")
df_train.Classe.value_counts()

## numerotation des classes
# Créer un dictionnaire de correspondance entre les classes et les valeurs numériques
classes_train = df_train['Classe'].unique()
class_dict_train = {cls: i for i, cls in enumerate(classes_train)}

# Assigner les valeurs numériques en fonction du dictionnaire
df_train['Classe'] = df_train['Classe'].map(class_dict_train)
##
scaler = MinMaxScaler(feature_range=(0, 3))
data_train = scaler.fit_transform(df_train[["Temperature", "Frequency", "Cpu_usage", "Cpu_memory",'Classe']])


##entrainement

n_steps = 100 # Nombre de pas pour chaque séquence
n_features = data_train.shape[1] - 1  # Nombre de caractéristiques sans la variable cible
num_classes = len(df_train['Classe'].unique())

# Préparation des données d'entraînement
X_train = []
y_train = []

for i in range(n_steps, len(df_train)):
    X_train.append(data_train[i - n_steps:i, :-1])
    y_train.append(data_train[i-1, -1])  # Récupérer la classe à prédire

##

X_train = np.array(X_train)
y_train = to_categorical(y_train, num_classes = num_classes)  # Convertir en catégories pour le modèle
##
# Modèle LSTM
model = Sequential()
model.add(LSTM(50, input_shape=(n_steps, n_features)))
model.add(Dense(num_classes, activation='softmax'))  # Activation softmax pour prédire parmi les classes
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model.fit(X_train, y_train, epochs=50, batch_size=32)
##
df_test = pd.read_csv(r"C:\Users\Administrator\Documents\EN_ENSEIGNE\PFE\RPI\DATASETS\MQTT_bruteforce2\cpu_stats.csv")
##numerotation des classes

# Créer un dictionnaire de correspondance entre les classes et les valeurs numériques
classes_test = df_test['Classe'].unique()
class_dict_test = {cls: i for i, cls in enumerate(classes_test)}

# Assigner les valeurs numériques en fonction du dictionnaire
df_test['Classe'] = df_test['Classe'].map(class_dict_test)

## mise en forme test
data_test = scaler.transform(df_test[["Temperature", "Frequency", "Cpu_usage", "Cpu_memory",'Classe']])
# Préparation des données de test
X_test = []
y_test = []
for i in range(0, len(df_test)):
    if i < n_steps:
        zeros_to_add = n_steps - i
        seq = np.vstack([np.zeros((zeros_to_add, n_features)), data_test[0:i + 1, :-1]])
        X_test.append(seq)
        y_test.append(data_test[i, -1])
    else:
        X_test.append(data_test[i - n_steps:i, :-1])
        y_test.append(data_test[i, -1])

# Utiliser pad_sequences pour harmoniser la longueur des séquences
X_test_padded = pad_sequences(X_test, maxlen=n_steps, dtype='float32', padding='pre')
y_test = to_categorical(y_test, num_classes=num_classes) # Convertir en catégories pour le modèle
##prediction

# Prédiction sur les données de test
y_pred = model.predict(X_test_padded)

# Récupérer la classe prédite pour chaque exemple
predicted_classes = np.argmax(y_pred, axis=1)

#true classes
true_classes = np.argmax(y_test, axis=1)

# Calcul de l'exactitude (accuracy)
accuracy = accuracy_score(np.argmax(y_test, axis=1), predicted_classes)
print(f'Exactitude : {accuracy}')
# Matrice de confusion
confusion = confusion_matrix(np.argmax(y_test, axis=1), predicted_classes)
print("Matrice de confusion :")
print(confusion)



##tracé des resultats
df_test['predicted_class'] = predicted_classes
df_test['true_class'] = true_classes

# Afficher le graphique
plt.figure(figsize=(10, 6))

# Créer des couleurs pour chaque classe prédite
colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'cyan'}  # Modifier en fonction du nombre de classes

# Tracer le graphique point par point en attribuant une couleur en fonction de la classe prédite
for label, color in colors.items():
    subset = df_test[df_test['predicted_class'] == label]
    plt.scatter(subset.index, subset['Cpu_usage'], label=f'Classe {label}', color=color)

plt.xlabel('Index')
plt.ylabel('Cpu_usage')
plt.legend()
plt.show()


## verif
unique_values_y_test = np.unique(y_test)
unique_values_predicted_classes = np.unique(predicted_classes)

print("Valeurs uniques dans y_test :", unique_values_y_test)
print("Valeurs uniques dans predicted_classes :", unique_values_predicted_classes)



