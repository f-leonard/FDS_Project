# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:11:05 2022

@author: 35387
"""
import random
import matplotlib
from tensorflow import keras
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from itertools import count
import pandas as pd 
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
from matplotlib.pyplot import show, plot


'''Index of semi-conductor stocks'''
ticker = '^SOX'
yticker = yf.Ticker(ticker)
stock_data = yticker.history(period="7d",interval = '1m') 

mpf.plot(stock_data,ylabel = 'Price (USD)',title = 'Plottitle', type ='line' )

'''semi_data = pd.read_csv('Semi_data.csv')
semi_data.index = semi_data['DATE']
semi_data = semi_data.iloc[300:]
semi_data['Import Price Index(in $ End Use of semiconductors)'] = semi_data['Import Price Index(in $ End Use of semiconductors)'].astype(float)
semi_data['Export Price Index(End Use of semiconductors)'] = semi_data['Export Price Index(End Use of semiconductors)'].astype(float)
'''

#%%

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
nvda_ticker = yf.Ticker('NVDA')
tsmc_data = tsmcticker.history(period = '8y',interval = '1wk')
intel_data = intel_ticker.history(period = '8y',interval = '1wk')
nvidia_data = nvda_ticker.history(period = '8y', interval = '1wk')
ticker = 'APTV'
apticker = yf.Ticker(ticker)
aptiv_data = apticker.history(period="8y",interval = '1wk')




mpf.plot(tsmc_data,ylabel = 'Price (USD)')
plt.title('Semiconductor Companies')
plt.ylabel('% Change in stock price')
plt.plot((tsmc_data['Close']/tsmc_data['Close'][0])*100-100,label = 'TSMC')
plt.plot((intel_data['Close']/intel_data['Close'][0])*100-100,label = 'Intel')
plt.plot((nvidia_data['Close']/nvidia_data['Close'][0])*100-100,label = 'NVDA')
plt.plot((aptiv_data['Close']/aptiv_data['Close'][0])*100-100, label = 'APTV')
#plt.use_style('ggplot')
plt.legend()
#%%
y1 = tsmc_data['Close']/tsmc_data['Close'][0]*100-100
y2 = intel_data['Close']/intel_data['Close'][0]*100-100
y3 = nvidia_data['Close']/nvidia_data['Close'][0]*100-100
t = range(int(len(y1)))
x,y,z,h=[], [], [],[]

fig = plt.figure(figsize = (12,8))
axes = fig.add_subplot(1,1,1)
#%%
def animate(i):
    x.append(intel_data.index[i])
    y.append(y1[i])
    z.append(y2[i])
    h.append(y3[i])
    plt.plot(x,y,scaley = True,scalex = True, color = "Blue")
    plt.plot(x,z, scaley = True, scalex = True, color = "Black")
    plt.plot(x,h, scaley = True, scalex = True, color = 'Green')
    plt.ylabel('% Change in price',fontsize=12)
    
    plt.legend(['TSMC','Intel','Nvidia'],loc = 'upper left')
    
    

anim = animation.FuncAnimation(fig=fig, func=animate, interval=1000, frames = 427,repeat = False)
f = r"C:\Users\35387\OneDrive - University College Dublin\Financial Data Science\FDS_Project\animation.gif" 
writergif = animation.PillowWriter(fps=15) 
anim.save(f, writer=writergif)
#%%
#What has happened to say NVDA has shown such great potential
semi_data['DATE'] = pd.to_datetime(semi_data['DATE'],format = '%YYYY/%mm/%dd')
print(stock_data.index)
stock_predictor = stock_data[stock_data.index.isin(semi_data['DATE'])]
#%%
mpf.plot(aptiv_data,title = 'APTV Stock', ylabel = 'Price (USD)')


#%%

