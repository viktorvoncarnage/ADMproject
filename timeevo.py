# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:48:03 2022

@author: DataStudio
"""

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


datosNO2 = pd.read_csv(r"C:\\Users\\albag\\Desktop\\Escritorio\\ADM\\datos\\datosNO2.csv",
                         index_col=0,
                         header=0)
# show loaded table:
datosNO2


# add datetime column with python datetimes
datosNO2["data_datetime"] = pd.to_datetime(datosNO2.data)

datosNO2=datosNO2.set_index('data_datetime')

#add daily mean
datosNO2['Daily Mean'] = datosNO2[['h01','h02','h03','h04','h05','h06','h07','h08','h09','h10',
                                   'h11','h12','h13','h14','h15','h16','h17','h18','h19','h20',
                                   'h21','h22','h23','h24']].mean(axis=1)



datosNO2


#subplots for the 12 measuring stations

plt.rcParams['figure.figsize'] = [20, 15]

for i, group in datosNO2.groupby("nom_estacio"):
    f, ax = plt.subplots()

    datosNO2estacion=datosNO2[datosNO2["nom_estacio"]==i]
    
    #for each station separately
    # calculating simple moving average
    # using .rolling(window).mean() ,
    # with window size = 30    
    # using .to_frame() to convert pandas series
    # into dataframe.
    datosNO2estacion = datosNO2estacion['Daily Mean'].to_frame()
    datosNO2estacion['Moving Mean'] = datosNO2estacion['Daily Mean'].rolling(30, min_periods=15,
                                                                             center=True).mean()
    datosNO2utiles=datosNO2estacion[['Moving Mean']]

    datosNO2utiles.plot(ax=ax, grid=True)

    ax.set_xticklabels(ax.get_xticklabels())

    ax.set_title(i)
    ax.set_xlabel('Datetime')
    ax.set_ylabel('NO2 (µg/m3)')
    
    ax.axvspan('2020-03-15', '2020-06-21', alpha=0.4, color='grey')
    ax.axvspan('2019-03-15', '2019-06-21', alpha=0.4, color='grey')
    
    
    

#studying seasonal frequency via fourier transforms 
#frequency representation of a time-dependent signal

import scipy as sp
import scipy.fftpack

#filter by station, one station
#at the begining it was eixample, the data periodicity was better observed in ciutadella but i didnt change the name of the variable

datosNO2eixample=datosNO2[datosNO2["nom_estacio"]=="Barcelona (Ciutadella)"]

# using .to_frame() to convert pandas series
# into dataframe.
datosNO2eixample = datosNO2eixample['Daily Mean'].to_frame()

datosNO2eixample['Moving Mean'] = datosNO2eixample['Daily Mean'].rolling(30, min_periods=15, 
                                                                         center=True).mean()


datosNO2eixampleutiles=datosNO2eixample[['Moving Mean']]
datosNO2eixampleutiles=datosNO2eixampleutiles[datosNO2eixampleutiles["Moving Mean"].notna()]

date = datosNO2eixampleutiles.index
mean = datosNO2eixampleutiles['Moving Mean']
N = len(mean)

#Fourier transform
mean_fft = sp.fftpack.fft(mean.values)

#power spectral density
mean_psd = np.abs(mean_fft) ** 2

#get the frequencies
#Here, we choose an annual unit: a frequency of 1 corresponds to 1 year (365 days)
#We provide 1/365 because the original unit is in days:
fftfreq = sp.fftpack.fftfreq(len(mean_psd), 1. / 365)

#We are only interested in positive frequencies here, as we have a real signal:
i = fftfreq > 0

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot(fftfreq[i], 10 * np.log10(mean_psd[i]))
ax.set_xlim(0, 5)
ax.set_xlabel('Frequency (1/year)')
ax.set_ylabel('PSD (dB)')

#Because the fundamental frequency of the signal is the yearly variation of the temperature, we observe a peak for f=1.
#Now, we cut out frequencies higher than the fundamental frequency:

mean_fft_bis = mean_fft.copy()
mean_fft_bis[np.abs(fftfreq) > 1.1] = 0

#Next, we perform an inverse FFT to convert the modified Fourier transform back to the temporal domain.
#This way, we recover a signal that mainly contains the fundamental frequency

plt.rcParams['figure.figsize'] = [20, 15]

mean_slow = np.real(sp.fftpack.ifft(mean_fft_bis))

fig, ax = plt.subplots(1, 1, figsize=(6, 3))
mean.plot(ax=ax, lw=.5)
ax.plot_date(date, mean_slow, '-')

ax.set_xlabel('Datetime')
ax.set_ylabel('NO2 (µg/m3)')
ax.set_title('Barcelona (Ciutadella)')

#We get a smoothed version of the signal,
#because the fast variations have been lost when we have removed the high frequencies in the Fourier transform.