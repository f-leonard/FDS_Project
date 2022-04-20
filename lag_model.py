# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 15:04:18 2022

@author: 35387
"""

import pandas as pd
import numpy as np
import datetime
import shutil
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
import yfinance as yf
def create_model():
  np.random.seed(100)
  tf.random.set_seed(100)
  return tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu',input_dim = len(cols)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])

df = yf.Ticker('APTV').history(period = '3y')
tsmc = yf.Ticker('TSM').history(period = '3y')
nvidia = yf.Ticker('NVDA').history(period = '3y')
intel = yf.Ticker('INTC').history(period = '3y', tz= None)
print(intel.index)
#%%
df = pd.DataFrame(df) # Empty DataFrame


df['Return'] = np.log(df['Close']/df['Close'].shift(1))
tsmc['Return'] = np.log(tsmc['Close']/tsmc['Close'].shift(1))
df['MA'] = df['Return'].rolling(5).mean()
df['TSMC_ret'] = tsmc['Return'].rolling(5).mean()
nvidia['Return'] = np.log(nvidia['Close']/nvidia['Close'].shift(1))
intel['Return'] = np.log(intel['Close']/intel['Close'].shift(1))
df['intel_ret'] = np.log(intel['Return'].rolling(5).mean())
df['NVDA_ret'] = nvidia['Return'].rolling(5).mean()


# create lagged returns
#%%
cols=[]
df.dropna(inplace=True)


df['direction'] = np.where(df['Return'] > 0, 1, 0)
cols.append('MA')
cols.append('TSMC_ret')
cols.append('NVDA_ret')
cols.append('intel_ret')
#%%

# split the dataset in training and test datasets
train, test = train_test_split(df.dropna(), test_size=0.4, shuffle=True)


# create the model
model = create_model()

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
r = model.fit(train[cols], 
              train['direction'], 
              epochs=5,
              validation_data=(test[cols], test['direction']), 
              callbacks=[tensorboard_callback]) #verbose=False
'''OUTPUT_DIR = "./export/savedmodel"
shutil.rmtree(OUTPUT_DIR,ignore_errors=True)
EXPORT_PATH = os.path.join(OUTPUT_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
tf.saved_model.save(model,EXPORT_PATH)'''

pred = model.predict(test[cols]) 
trade = pred > 0.5 + pred.std()
profits = test.loc[trade, 'Return'] 
print('Scheme Info. Ratio:' + "{:.2f}".format(np.sqrt(365)*profits.mean()/profits.std()))
print('Underlying Info. Ratio:' + "{:.2f}".format(np.sqrt(365)*test['Return'].mean()/test['Return'].std()))

#scheme info = avg yearly profits/standard deviation
#underlying ratio = test['Return]
