# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 00:07:09 2023

@author: spika
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow import keras

# Load data into a DataFrame
df = pd.read_csv('out_new.csv')

# Drop the match_id column
df.drop(columns=['match_id'], inplace=True)


# Extract the categorical features
cat_cols = ['tier_b1', 'rank_b1', 
            'tier_b2', 'rank_b2', 
            'tier_b3', 'rank_b3', 
            'tier_b4', 'rank_b4', 
            'tier_b5', 'rank_b5', 
            
            'tier_r1', 'rank_r1', 
            'tier_r2', 'rank_r2', 
            'tier_r3', 'rank_r3', 
            'tier_r3.1', 'rank_r3.1', 
            'tier_r3.2', 'rank_r3.2', 
            
            ]


#creating instance
encoder = OneHotEncoder(handle_unknown='ignore')

#perform one-hot encoding on 'team' column
encoder_df = pd.DataFrame(encoder.fit_transform(df[cat_cols]).toarray())

#merge the dfs
final_df = df.drop(columns=cat_cols).join(encoder_df)
 # 'veteran_r5', 'inactive_r5', 'freshBlood_r5', 'hotStreak_r5'


# Split data into input features and target variable
X = final_df.drop(columns=['blueTeam_win'])
y = final_df['blueTeam_win']


# X.replace('False', 0)
# X.replace('True', 1, inplace=True)
# Normalize the continuous features
#...




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