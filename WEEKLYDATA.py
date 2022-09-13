#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:30:15 2022

@author: mbalague
"""
# LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# PRINCIPAL FUNCTIONS 
def read(nomfitxer):
    """
    opens a csv file, saves it as a data frame with only the columns that have precipitation values and the recorded time
    it also checks the verification state of the data and only returns the data frame with verified data
    'nomfitxer' has to have the following format: STATIONCODE_CLIMATICCONSTANTCODE.csv
    """
    
    df_original = pd.read_csv(nomfitxer, delimiter = ';') 
    df_div = df_original[['DATA_LECTURA','DATA_EXTREM','VALOR_LECTURA','CODI_ESTAT']]
    df_div['DATA'] = pd.to_datetime(df_div['DATA_LECTURA'], dayfirst = True)
    df_div['EXTREMS'] = pd.to_datetime(df_div['DATA_EXTREM'],dayfirst = True)
    
    
    #QUALITY CONTROL
    length_llista = df_div.size
    
    df_revised = df_div.loc[df_original['CODI_ESTAT']=='V'] #V for verified values
    length_v = df_revised.size
    if length_v >= 0.8*length_llista:
        df = df_revised[['DATA','EXTREMS','VALOR_LECTURA','CODI_ESTAT']]
        return df
    else:
       print('DOES NOT PASS QUALITY CONTROL GUIDELINES')
       
 
def select_year(df,year):
    """
    divides the data frame we select into yearly ones
    'year' has to be between [2009,2022]
    the date column now acts as the index of the data frame
    returns a new data frame with 3 columns (registered date of the extrem value if there is one, variable value, verification state of the value)
    """
    filt = (df['DATA'] >= pd.to_datetime(str(year)+'-01-01')) & (df['DATA'] < pd.to_datetime(str(year+1)+'-01-01'))
    df_years = df.loc[filt]
    df_years = df_years.sort_values('DATA',ascending = True)
    df_years = df_years.set_index('DATA')
    return df_years


def select_week(nomfitxer,year):
    """
    adds a columns to the data frame with the week number associated to each value
    returns the new data frame as well as an array with the week numbers
    """
    df = select_year(read(nomfitxer),year)
    df['WEEK_NUM'] = pd.DatetimeIndex(df.index).isocalendar().week 
    return df, df['WEEK_NUM']

def weekly_mean(nomfitxer,year):
    """
    passing a yearly data frame, returns a list with the weekly mean values
    """
    means = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('W').mean()
    return means


def maxmin(nomfitxer,year,select):
    """
    returns the extrem weekly value for a specific year
    select has to be eiter 'max' or 'min' (string values)
    """
    if select == 'max':
        extrem = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('W').max()
    if select == 'min':
        extrem = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('W').min()
    
    return extrem.mean()

def climatic_weekly_means(nomfitxer):
    """
    returns the weekly mean for the period 2010-2019
    """    
    means = np.array([])
    a = weekly_mean(nomfitxer,2010)
    b = weekly_mean(nomfitxer,2011)
    c = weekly_mean(nomfitxer,2012)
    d = weekly_mean(nomfitxer,2013)
    e = weekly_mean(nomfitxer,2014)
    f = weekly_mean(nomfitxer,2015)
    g = weekly_mean(nomfitxer,2016)
    h = weekly_mean(nomfitxer,2017)
    j = weekly_mean(nomfitxer,2018)
    k = weekly_mean(nomfitxer,2019)
        
    for i in range(0,53):
        means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))
   
    return means

#%% NOT FINISHED / VALIDATED 
def extrems(nomfitxer,year,week,select):
    """
    i wanted to generate a function that could
    primarly get the weekly extrem values for a selected year 
    and return it as an array of values. the code works but 
    raises an error / don't know if the result is correct.
    """
    extrem_list = np.array([])
    for i in range(1,54):
        if select_week(nomfitxer,year)[1] == i:
            extrem_list = np.append(extrem_list,select_week(nomfitxer,year)['WEEK_NUM' == i])
    return extrem_list

#%% WEEKLY TEMPERATURE GRAPH
plt.style.use('ggplot')

plt.figure('Weekly Tàrrega 2021')
plt.grid(True)
plt.title('Tàrrega')
setmanes = ['04-07','11-07','18-07','25-07','01-08','08-08','15-08','22-08','29-08']
#IN ORDER TO GRAPH WE NEED TO KNOW THE START AND END OF EACH WEEK AND ITS WEEK NUMBER 
plt.plot(setmanes,weekly_mean('C7_32.csv',2021)[26:35], label = 'TMm 2021' ,linestyle = 'solid', marker = 'o', color = 'maroon')
plt.plot(setmanes,climatic_weekly_means('C7_32.csv')[26:35],label = 'TMm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'red' )
plt.plot(setmanes,extrems('C7_40.csv',2021,26,'max'), label = 'TXm 2021',linestyle = 'solid', marker = 'o', color = 'firebrick')
plt.plot(setmanes,extrems('C7_42.csv',2021,26,'min'), label = 'TNm 2021',linestyle = 'solid', marker = 'o', color = 'lightcoral')


plt.legend(loc = 8)
plt.xlabel('Weeks')
plt.ylabel('Temperature (°C)')
#plt.savefig('Weekly Tàrrega 2021.png', format='png', dpi=800)
plt.tight_layout()
