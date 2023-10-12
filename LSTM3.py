import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

## Charger votre dataset
df_train = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\normal\cpu_stats.csv", names=["Temps", "Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])
df_test = pd.read_csv(r"C:\Users\Administrator\Documents\EN ENSEIGNE\PFE\RPI\attaque1_bruteforce\cpu_stats.csv", names=["Temps", "Temperature", "Frequency", "Cpu_usage", "Cpu_memory"])
## Mise à l'échelle des données (dans la plage 0-1)
scaler = MinMaxScaler(feature_range=(0, 1))
data_train = scaler.fit_transform(df_train[["Temperature", "Frequency", "Cpu_usage", "Cpu_memory"]])
data_test = scaler.fit_transform(df_test[["Temperature", "Frequency", "Cpu_usage", "Cpu_memory"]])

## Définir la longueur des séquences temporelles et le nombre de caractéristiques
n_steps = 10  # Ajustez la longueur des séquences en fonction de votre problème
n_features = data_train.shape[1]  # Nombre de caractéristiques (Temperature, Frequency, Cpu_usage, Cpu_memory)

## Conversion des données en séquences temporelles
X, y = [], []
for i in range(n_steps, len(data)):
    X.append(data[i - n_steps:i, :])
    y.append(data[i, :])  # Prédiction de toutes les caractéristiques
X, y = np.array(X), np.array(y)


## Divisez les données en ensembles de formation et de test
split_ratio = 0.8
split_index = int(len(X) * split_ratio)
X_train, X_test, y_train, y_test = X[:split_index], X[split_index:], y[:split_index], y[split_index:]

## dans le cas de deux dataset
# Conversion des données en séquences temporelles

X_train, y_train = [], []
for i in range(n_steps, len(data_train)):
    X_train.append(data_train[i - n_steps:i, :])
    y_train.append(data_train[i, :])  # Prédiction de toutes les caractéristiques
X_train, y_train = np.array(X_train), np.array(y_train)

X_test, y_test = [], []
for i in range(n_steps, len(data_test)):
    X_test.append(data_test[i - n_steps:i, :])
    y_test.append(data_test[i, :])  # Prédiction de toutes les caractéristiques
X_test, y_test = np.array(X_test), np.array(y_test)

## Créez le modèle LSTM
model = Sequential()
model.add(LSTM(50, input_shape=(n_steps, n_features)))
model.add(Dense(n_features))  # Vous prédisez toutes les caractéristiques
model.compile(optimizer='adam', loss='mean_squared_error')

## Entraînez le modèle
model.fit(X_train, y_train, epochs=50, batch_size=32)

## Prédisez les caractéristiques pour l'ensemble de test
y_pred = model.predict(X_test)

# Inversez la mise à l'échelle des prédictions
y_pred = scaler.inverse_transform(y_pred)
y_test = scaler.inverse_transform(y_test)

##Tracez les prédictions pour toutes les caractéristiques
# Tracez les prédictions pour chaque feature
# Visualisez les prédictions
for i in range(n_features):
    plt.figure(figsize=(12, 6))
    plt.plot(y_test[:, i], label=f'{df.columns[i+1]} réelle')
    plt.plot(y_pred[:, i], label=f'{df.columns[i+1]} prédite')
    plt.legend()
    plt.title(f'Prédiction de {df.columns[i+1]}')
    plt.show()