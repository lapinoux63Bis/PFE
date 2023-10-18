import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

##

# Charger votre dataset, supposons que vous avez une colonne 'time' et une colonne 'temperature'
# Assurez-vous que votre dataset est trié par ordre chronologique si ce n'est pas déjà le cas
df_test = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_nmap\TCPU\TCPU2", names = ["Temps","Temperature"])
df_train = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\TCPU\TCPU2", names = ["Temps","Temperature"])

# Extrait la colonne 'temperature' pour la prédiction
data_train = df_train['Temperature'].values.reshape(-1, 1)
data_test = df_test['Temperature'].values.reshape(-1, 1)

# Mise à l'échelle des données (dans la plage 0-1)
scaler = MinMaxScaler(feature_range=(0, 1))
data_train = scaler.fit_transform(data_train)
data_test = scaler.transform(data_test)  # N'utilisez pas fit_transform ici pour utiliser la même mise à l'échelle

# Définir la longueur des séquences temporelles et le nombre de caractéristiques (uniquement la température)
n_steps = 50  # Vous pouvez ajuster la longueur des séquences en fonction de votre problème
n_features = 1

# Conversion des données en séquences temporelles
X_train, y_train = [], []
for i in range(n_steps, len(data_train)):
    X_train.append(data_train[i - n_steps:i, 0])
    y_train.append(data_train[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_test, y_test = [], []
for i in range(n_steps, len(data_test)):
    X_test.append(data_test[i - n_steps:i, 0])
    y_test.append(data_test[i, 0])
X_test, y_test = np.array(X_test), np.array(y_test)

# Créez le modèle LSTM
model = Sequential()
model.add(LSTM(50, input_shape=(n_steps, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraînez le modèle
model.fit(X_train, y_train, epochs=50, batch_size=32)

## Prédisez les températures pour l'ensemble de test
y_pred = model.predict(X_test)
y_test = y_test.reshape(-1, 1)
## Inversez la mise à l'échelle des prédictions
y_pred = scaler.inverse_transform(y_pred)
y_test = scaler.inverse_transform(y_test)

## Tracez les prédictions
plt.figure(figsize=(12, 6))
plt.plot(y_test, label='Température réelle')
plt.plot(y_pred, label='Température prédite')
plt.legend()
plt.show()

###
# Calcul de la différence entre les températures réelles et prédites
differences = y_test - y_pred

# Spécifiez un seuil pour définir ce qui est "très différent"
seuil = 4.0  # Vous pouvez ajuster ce seuil en fonction de vos besoins

# Sélectionnez les indices où les différences dépassent le seuil
indices_anomalies = np.where(np.abs(differences) > seuil)[0]

# Affichez les températures réelles, prédites et les anomalies
plt.figure(figsize=(12, 6))
plt.plot(y_test, label='Température réelle')
plt.plot(y_pred, label='Température prédite')

# Marquez les anomalies
plt.scatter(indices_anomalies, y_test[indices_anomalies], color='red', label='Anomalies')

plt.legend()
plt.show()
