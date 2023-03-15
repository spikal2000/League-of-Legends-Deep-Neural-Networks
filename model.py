# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:35:17 2023

@author: spika
"""
import pandas as pd
import numpy as np
from numpy import genfromtxt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow import keras

# Load the dataset
data = pd.read_csv('data_file_1.csv')

X = data.iloc[:, 2:161]
y =  data['blueTeam_win']


# Apply log transformation to the input features
X = np.log(X + 1)
# Normalize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = keras.Sequential([
    keras.layers.Dense(250, activation='sigmoid', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(160, activation='sigmoid'),
    keras.layers.Dense(15, activation='sigmoid'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model with Adam optimizer
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=150, batch_size=45, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test accuracy:', test_acc)


# Use the model to make predictions on new data
new_data = pd.read_csv('data_file_1.csv')
X_new = scaler.transform(new_data.iloc[0:1, 2:161])
# y_new = new_data['blueTeam_win']

predictions = model.predict(X_new)
# test_loss, test_acc = model.evaluate(X_new, y_new)
# print('Test accuracy:', test_acc)
# Evaluate the performance of the model on the new data
# accuracy = accuracy_score(y_new, predictions.round())
# precision = precision_score(y_new, predictions.round())
# recall = recall_score(y_new, predictions.round())
# f1 = f1_score(y_new, predictions.round())
# binary_predictions = predictions.round()
# print('Accuracy: {:.2f}'.format(accuracy))
# print('Precision: {:.2f}'.format(precision))
# print('Recall: {:.2f}'.format(recall))
# print('F1 score: {:.2f}'.format(f1))