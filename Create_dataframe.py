# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 11:58:51 2022

@author: 35387
"""

import pandas as pd
import matplotlib.pyplot as plt
import shutil
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
import yfinance as yf
from scipy import interpolate
import datetime
vehicle_sales = pd.read_csv('TOTALSA.csv')
vehicle_sales['observation_date'] = pd.to_datetime(vehicle_sales['observation_date'])
vehicle_sales =vehicle_sales.set_index('observation_date')
industrial_metal = pd.read_csv('PerformanceGraphExport.csv')

print(industrial_metal.head())

industrial_metal['DATE'] = pd.to_datetime(industrial_metal['DATE'].astype(str),format = '%d/%m/%Y')
industrial_metal = industrial_metal.set_index('DATE')
vehicle_sales= vehicle_sales.iloc[519:-1]
plt.plot(industrial_metal['DATA'],label = 'metal')
plt.plot(vehicle_sales['TOTALSA'],label = 'car sales')

vehicle_sales['pct_sales'] = vehicle_sales['TOTALSA']/vehicle_sales['TOTALSA'][0]*100-100
industrial_metal['price'] = industrial_metal['DATA']/industrial_metal['DATA'][0]*100-100
plt.show()
plt.plot(vehicle_sales['pct_sales'],label = 'vehicle sales')
plt.plot(industrial_metal['price'],label = 'industrial metal cost')
plt.ylabel('% Change')
plt.xticks(rotation = 45)
plt.legend()
plt.title('New Car Sales and Industrial Metal Costs')

#%%

start = '2019-05-01'
end = '2022-04-01'

aptiv_df = yf.download('APTV',start = start ,end = end )
nvda_df = yf.download('NVDA',start =start, end = end )
aptiv_df['num'] = np.arange(len(aptiv_df))

x = vehicle_sales['number']
y = vehicle_sales['TOTALSA']

vehicle_sales['number'] = np.arange(len(vehicle_sales))
simulate = np.linspace(vehicle_sales['number'].min(),vehicle_sales['number'].max(),len(aptiv_df))
x = vehicle_sales['number']
y = vehicle_sales['TOTALSA']
f = interpolate.interp1d(x, y)

xnew = simulate
ynew = f(xnew)

noise = np.random.normal(0, 0.2,np.size(ynew))
ynew = ynew+noise


aptiv_df['car_sales'] = ynew
aptiv_df['NVDA'] = nvda_df['Close']

industrial_metal['number'] = np.arange(len(industrial_metal))
x = industrial_metal['number']
y = industrial_metal['DATA']
f = interpolate.interp1d(x, y)



simulate = np.linspace(industrial_metal['number'].min(),industrial_metal['number'].max(),len(aptiv_df))

xnew = simulate
ynew = f(xnew)

noise = np.random.normal(0, 0.2,np.size(ynew))
ynew = ynew+noise

aptiv_df['Industrial_metal'] = ynew

aptiv_df.to_csv('Aptiv_data_predictors.csv')