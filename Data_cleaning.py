# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:11:05 2022

@author: 35387
"""
import random
import matplotlib
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from itertools import count
import pandas as pd 
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
%matplotlib qt
'''Index of semi-conductor stocks'''
ticker = '^SOX'
yticker = yf.Ticker(ticker)
stock_data = yticker.history(period="10y") 

mpf.plot(stock_data,ylabel = 'Price (USD)',title = 'Plottitle', type ='line' )

semi_data = pd.read_csv('Semi_data.csv')
semi_data.index = semi_data['DATE']
semi_data = semi_data.iloc[300:]
semi_data['Import Price Index(in $ End Use of semiconductors)'] = semi_data['Import Price Index(in $ End Use of semiconductors)'].astype(float)
semi_data['Export Price Index(End Use of semiconductors)'] = semi_data['Export Price Index(End Use of semiconductors)'].astype(float)




plt.figure(0)

semi_data.plot(
    y = ['Export Price Index(End Use of semiconductors)','Import Price Index(in $ End Use of semiconductors)'])

plt.title('Export Vs Import Price index (USD)')
plt.xticks(rotation = 45)
plt.show()
semi_data['Exp/Imp_diff'] = semi_data['Export Price Index(End Use of semiconductors)']-semi_data['Import Price Index(in $ End Use of semiconductors)'] 
plt.figure(1)
semi_data.plot(y=['Exp/Imp_diff'])
plt.xticks(rotation = 45)
plt.ylabel('Difference (USD) between Export and Import')
plt.title('Semiconductor Price Index')
plt.show()

semi_data.plot(y = ['Producer Price Index(By  Industry in $)'])
plt.xticks(rotation = 45)

#In recent years the difference between the export price and import price has become positive indicating that there is a supply chain shortage

#%%
tsmcticker = yf.Ticker('TSM')
intel_ticker = yf.Ticker('INTC')
tsmc_data = tsmcticker.history(period = '10y', interval = "1wk")
intel_data = intel_ticker.history(period = '10y', interval = "1wk")

mpf.plot(tsmc_data,ylabel = 'Price (USD)')

plt.plot(tsmc_data['Close'],label = 'TSMC')
plt.plot(intel_data['Close'],label = 'Intel')
plt.legend()
#%%
y1 = tsmc_data['Close']
t = range(int(len(y1)))
x,y=[], []

fig = plt.figure(figsize = (12,8))
axes = fig.add_subplot(1,1,1)

def animate(i):
    x.append(t[i])
    y.append(y1[i])
    plt.plot(x,y,scaley = True,scalex = True, color = "Blue")

ani = FuncAnimation(fig=fig, func=animate, interval=1)
