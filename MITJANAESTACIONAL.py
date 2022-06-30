#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:12:20 2022

@author: mbalague
"""
# LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_name = str(input('FILE NAME: '))
format_csv = '.csv'
months_names = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
seasons_names = ['DJF','MAM','JJA','SON']

# CLIMATIC CONSTANTS CODE
TMm = '32'   
TXm = '40'
TNm = '42'
PPT = '35'
PPTx1h = '72'

# STATIONS CODE
poal = 'V8'
golmes = 'WC'
mollerussa = 'XI'
castellnou = 'C6'
tornabous = 'VR'
tarrega = 'C7'
santmarti = 'WL'
canos = 'VD'
cervera = 'C8'

# USER FRIENDLY MODE BY CONSOLE
if format_csv not in file_name:
    print('NO FILE WITH THIS NAME. TRY AGAIN.')
    file_name = str(input('FILE NAME: '))
    
if TMm in file_name:
    cc = 'TMm'  
elif PPT in file_name:
    cc = 'PPT'
elif PPTx1h in file_name:
    cc = 'PPT1xh'
if TXm in file_name:
    cc = 'TXm'
if TNm in file_name:
    cc = 'TNm'
   
if tarrega in file_name:
    location = 'Tàrrega'
elif poal in file_name:
    location = 'El Poal'
elif golmes in file_name:
    location = 'Golmés'
elif mollerussa in file_name:
    location = 'Mollerussa'
elif castellnou in file_name:
    location = 'Castellnou de Seana'
elif tornabous in file_name:
    location = 'Tornabous'
elif santmarti in file_name:
    location = 'Sant Martí de Riucorb'
elif canos in file_name:
    location = 'El Canós'
elif cervera in file_name:
    location = 'Cervera'  
    

selected_year = int(input('YEAR OF STUDY: '))   
if selected_year > 2022:
    print('YEAR NOT IN AVAILABLE RANGE. TRY AGAIN.')
    selected_year = int(input('YEAR OF STUDY: '))
if selected_year < 2010:
    print('YEAR NOT IN AVAILABLE RANGE. TRY AGAIN.')
    selected_year = int(input('YEAR OF STUDY: '))
if len(str(selected_year)) < 4:
    print('YEAR NOT AVAILABLE. TRY AGAIN.')
    selected_year = int(input('YEAR OF STUDY: '))
if len(str(selected_year)) > 4:
    print('YEAR NOT AVAILABLE. TRY AGAIN.')
    selected_year = int(input('YEAR OF STUDY: '))


# PRINCIPAL FUNCTIONS

def read(nomfitxer):
    """
    opens a csv file, saves it as a data frame with only the columns that have tempterature or precipitation values 
    and the recorded time.
    it also checks the verification state of the data and only returns the data frame with verified data
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
       

def seasonal(nomfitxer,year):
    """
    opens the data frame created with read()
    separates it by year (user selected) and into the 4 meteorological seasons
    returns the data frames as well as an array with the sum of the values for each column of each data frame
    """
    df = read(nomfitxer)
    
    winter = (df['DATA'] >= pd.to_datetime(str(year-1)+'-12-01')) & (df['DATA'] < pd.to_datetime(str(year)+'-03-01'))
    df_winter = df.loc[winter]
    df_winter = df_winter.sort_values('DATA',ascending = True)
    df_winter = df_winter.set_index('DATA')
    

    spring = (df['DATA'] >= pd.to_datetime(str(year)+'-03-01')) & (df['DATA'] < pd.to_datetime(str(year)+'-06-01'))
    df_spring = df.loc[spring]
    df_spring = df_spring.sort_values('DATA',ascending = True)
    df_spring = df_spring.set_index('DATA')
    
    summer = (df['DATA'] >= pd.to_datetime(str(year)+'-06-01')) & (df['DATA'] < pd.to_datetime(str(year)+'-09-01'))
    df_summer = df.loc[summer]
    df_summer = df_summer.sort_values('DATA',ascending = True)
    df_summer = df_summer.set_index('DATA')
    
    
    fall = (df['DATA'] >= pd.to_datetime(str(year)+'-09-01')) & (df['DATA'] < pd.to_datetime(str(year)+'-12-01'))
    df_fall = df.loc[fall]
    df_fall = df_fall.sort_values('DATA',ascending = True)
    df_fall = df_fall.set_index('DATA')
    
    seasons_SUM = np.array([])
    seasons_SUM = np.append(seasons_SUM,(df_winter['VALOR_LECTURA'].sum(),df_spring['VALOR_LECTURA'].sum(),df_summer['VALOR_LECTURA'].sum(),df_fall['VALOR_LECTURA'].sum()))
    
    return df_winter,df_spring, df_summer, df_fall, seasons_SUM


def climatic_values(nomfitxer):
    """
    using seasonal() we get the values for each season and for each year in the 2010-2019 period
    returns 4 data frames with the values for each individual season as well as an array with the mean for the overall seasons
    """    
    means = np.array([])
     
    
    a = seasonal(nomfitxer,2010)[4]
    b = seasonal(nomfitxer,2011)[4]
    c = seasonal(nomfitxer,2012)[4]
    d = seasonal(nomfitxer,2013)[4]
    e = seasonal(nomfitxer,2014)[4]
    f = seasonal(nomfitxer,2015)[4]
    g = seasonal(nomfitxer,2016)[4]
    h = seasonal(nomfitxer,2017)[4]
    j = seasonal(nomfitxer,2018)[4]
    k = seasonal(nomfitxer,2019)[4]
                
    winter_mean = (a[0]+b[0]+c[0]+d[0]+e[0]+f[0]+g[0]+h[0]+j[0]+k[0])/10
    spring_mean = (a[1]+b[1]+c[1]+d[1]+e[1]+f[1]+g[1]+h[1]+j[1]+k[1])/10
    summer_mean = (a[2]+b[2]+c[2]+d[2]+e[2]+f[2]+g[2]+h[2]+j[2]+k[2])/10
    fall_mean = (a[3]+b[3]+c[3]+d[3]+e[3]+f[3]+g[3]+h[3]+j[3]+k[3])/10
    means = np.append(means,(winter_mean,spring_mean,summer_mean,fall_mean))
   
    w1 = seasonal(nomfitxer,2010)[0]
    w2 = seasonal(nomfitxer,2011)[0]
    w3 = seasonal(nomfitxer,2012)[0]
    w4 = seasonal(nomfitxer,2013)[0]
    w5 = seasonal(nomfitxer,2014)[0]
    w6 = seasonal(nomfitxer,2015)[0]
    w7 = seasonal(nomfitxer,2016)[0]
    w8 = seasonal(nomfitxer,2017)[0]
    w9 = seasonal(nomfitxer,2018)[0]
    w10 = seasonal(nomfitxer,2019)[0]
    winter = pd.concat([w1,w2,w3,w4,w5,w6,w7,w8,w9,w10])

    sp1 = seasonal(nomfitxer,2010)[1]
    sp2 = seasonal(nomfitxer,2010)[1]
    sp3 = seasonal(nomfitxer,2010)[1]
    sp4 = seasonal(nomfitxer,2010)[1]
    sp5 = seasonal(nomfitxer,2010)[1]
    sp6 = seasonal(nomfitxer,2010)[1]
    sp7 = seasonal(nomfitxer,2010)[1]
    sp8 = seasonal(nomfitxer,2010)[1]
    sp9 = seasonal(nomfitxer,2010)[1]
    sp10 = seasonal(nomfitxer,2010)[1]
    spring = pd.concat([sp1,sp2,sp3,sp4,sp5,sp6,sp7,sp8,sp9,sp10])
    
    
    s1 = seasonal(nomfitxer,2010)[2]
    s2 = seasonal(nomfitxer,2010)[2]
    s3 = seasonal(nomfitxer,2010)[2]
    s4 = seasonal(nomfitxer,2010)[2]
    s5 = seasonal(nomfitxer,2010)[2]
    s6 = seasonal(nomfitxer,2010)[2]
    s7 = seasonal(nomfitxer,2010)[2]
    s8 = seasonal(nomfitxer,2010)[2]
    s9 = seasonal(nomfitxer,2010)[2]
    s10 = seasonal(nomfitxer,2010)[2]
    summer = pd.concat([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10])
    
    
    
    f1 = seasonal(nomfitxer,2010)[3]
    f2 = seasonal(nomfitxer,2010)[3]
    f3 = seasonal(nomfitxer,2010)[3]
    f4 = seasonal(nomfitxer,2010)[3]
    f5 = seasonal(nomfitxer,2010)[3]
    f6 = seasonal(nomfitxer,2010)[3]
    f7 = seasonal(nomfitxer,2010)[3]
    f8 = seasonal(nomfitxer,2010)[3]
    f9 = seasonal(nomfitxer,2010)[3]
    f10 = seasonal(nomfitxer,2010)[3]
    fall = pd.concat([f1,f2,f3,f4,f5,f6,f7,f8,f9,f10])
    
    return winter, spring, summer, fall, means


#%% MONTHLY PRECIPITATION GRAPH COMPARING ALL THE STATIONS FOR THE SAME YEAR

r = np.arange(4)
width = 0.10
plt.style.use('ggplot')
plt.grid(True)

plt.bar(r, seasonal('WL_35.csv',2021)[4], color = 'lightcoral', width = width, edgecolor = None, label='Sant Martí de Riucorb') 
plt.bar(r+width, seasonal('C7_35.csv',2021)[4], color = 'indianred', width = width, edgecolor = None, label='Tàrrega')  
plt.bar(r+2*width, seasonal('VD_35.csv',2021)[4], color = 'firebrick', width = width, edgecolor = None, label='El Canós') 
plt.bar(r+3*width, seasonal('C8_35.csv',2021)[4], color = 'maroon', width = width, edgecolor = None,  label='Cervera')  
plt.bar(r+4*width, seasonal('V8_35.csv',2021)[4], color = 'lightgreen', width = width, edgecolor = None, label='El Poal')
plt.bar(r+5*width, seasonal('XI_35.csv',2021)[4], color = 'limegreen', width = width, edgecolor = None, label='Mollerussa')
plt.bar(r+6*width, seasonal('WC_35.csv',2021)[4], color = 'seagreen', width = width, edgecolor = None, label='Golmés')
plt.bar(r+7*width, seasonal('C6_35.csv',2021)[4], color = 'darkgreen', width = width, edgecolor = None, label='Castellnou de Seana')

plt.ylabel("Monthly precipitation (mm)")
plt.title("2021")
plt.grid(True)
plt.xticks(r + 3*width,seasons_names)
plt.legend(loc = 9)

#%% SEASONAL PRECIPITATION GRAPH USING ALL THE STATIONS FOR THE 2010-2019 TIME SERIES

r = np.arange(4)
width = 0.08
plt.style.use('ggplot')
plt.grid(True)
  
plt.bar(r, climatic_values('WL_35.csv')[4], color = 'lightcoral', width = width, edgecolor = None, label='Sant Martí de Riucorb')  
plt.bar(r+width, climatic_values('C7_35.csv')[4], color = 'indianred', width = width, edgecolor = None, label='Tàrrega') 
plt.bar(r+2*width, climatic_values('VD_35.csv')[4], color = 'firebrick', width = width, edgecolor = None, label='El Canós')  
plt.bar(r+3*width,climatic_values('C8_35.csv')[4], color = 'maroon', width = width, edgecolor = None, label='Cervera')  

plt.bar(r+4*width, climatic_values('V8_35.csv')[4], color = 'lightgreen', width = width, edgecolor = None, label='El Poal')
plt.bar(r+5*width, climatic_values('XI_35.csv')[4], color = 'limegreen', width = width, edgecolor = None, label='Mollerussa')
plt.bar(r+6*width, climatic_values('WC_35.csv')[4], color = 'seagreen', width = width, edgecolor = None, label='Golmés')
plt.bar(r+7*width, climatic_values('C6_35.csv')[4], color = 'darkgreen', width = width, edgecolor = None, label='Castellnou de Seana')

plt.ylabel("Seasonal precipitation (mm)")
plt.title("2010-2019")
plt.grid(True)
plt.xticks(r + 3*width,seasons_names)
plt.legend(loc = 2)