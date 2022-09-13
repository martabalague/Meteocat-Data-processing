#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:57:01 2022

@author: mbalague
"""

# GENERATOR OF THE JSON MONTHLY AEMET DATA

import http.client
conn = http.client.HTTPSConnection("opendata.aemet.es")
headers = {'cache-control': "no-cache"}

conn.request("GET", "/opendata/api/valores/climatologicos/diarios/datos/fechaini/2019-12-01T00%3A00%3A00UTC/fechafin/2019-12-31T23%3A59%3A59UTC/todasestaciones/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYmFsYWd1ZUBtZXRlby51Yi5lZHUiLCJqdGkiOiI0MmUwYTViOS0wNWY5LTRjZTQtYTRjZS1lMjgxODc5ODdiMzgiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY1NTgxMTM0NywidXNlcklkIjoiNDJlMGE1YjktMDVmOS00Y2U0LWE0Y2UtZTI4MTg3OTg3YjM4Iiwicm9sZSI6IiJ9.mAcOireHMLVSe-GkymG0A81Q6EaiqNTTWtF_saxraYk", headers=headers)

#api key --> 'https://opendata.aemet.es/centrodedescargas/altaUsuario?'
#format data --> fechaini/2021-12-01T00%3A00%3A00UTC/fechafin/2021-12-31T23%3A59%3A59UTC

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


months_names = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
months_list = ['01','02','03','04','05','06','07','08','09','10','11','12']


def data(city):
    """"
    opens the files (can be modified), obtains the target data (values and dates)
    returns two data frames with the values for LLEIDA and MANRESA
    """
    
    df_1 = pd.read_csv('ENERO 2021.csv', delimiter = ',', decimal = ',') 
    df_2 = pd.read_csv('FEBRERO 2021.csv', delimiter = ',', decimal = ',') 
    df_3 = pd.read_csv('MARZO 2021.csv', delimiter = ',', decimal = ',') 
    df_4 = pd.read_csv('ABRIL 2021.csv', delimiter = ',', decimal = ',') 
    df_5 = pd.read_csv('MAYO 2021.csv', delimiter = ',', decimal = ',') 
    df_6 = pd.read_csv('JUNIO 2021.csv', delimiter = ',', decimal = ',') 
    df_7 = pd.read_csv('JULIO 2021.csv', delimiter = ',', decimal = ',') 
    df_8 = pd.read_csv('AGOSTO 2021.csv', delimiter = ',', decimal = ',') 
    df_9 = pd.read_csv('SEPTIEMBRE 2021.csv', delimiter = ',', decimal = ',') 
    df_10 = pd.read_csv('OCTUBRE 2021.csv', delimiter = ',', decimal = ',') 
    df_11 = pd.read_csv('NOVIEMBRE 2021.csv', delimiter = ',', decimal = ',') 
    df_12 = pd.read_csv('DICIEMBRE 2021.csv', delimiter = ',', decimal = ',') 
    
    df_1['DATA'] = pd.to_datetime(df_1['fecha'], dayfirst = True)
    df_gen = df_1.set_index('DATA')
    df_2['DATA'] = pd.to_datetime(df_2['fecha'], dayfirst = True)
    df_feb = df_2.set_index('DATA')
    df_3['DATA'] = pd.to_datetime(df_3['fecha'], dayfirst = True)
    df_mar = df_3.set_index('DATA')
    df_4['DATA'] = pd.to_datetime(df_4['fecha'], dayfirst = True)
    df_apr = df_4.set_index('DATA')
    df_5['DATA'] = pd.to_datetime(df_5['fecha'], dayfirst = True)
    df_may = df_5.set_index('DATA')
    df_6['DATA'] = pd.to_datetime(df_6['fecha'], dayfirst = True)
    df_jun = df_6.set_index('DATA')
    df_7['DATA'] = pd.to_datetime(df_7['fecha'], dayfirst = True)
    df_jul = df_7.set_index('DATA')
    df_8['DATA'] = pd.to_datetime(df_8['fecha'], dayfirst = True)
    df_aug = df_8.set_index('DATA')
    df_9['DATA'] = pd.to_datetime(df_9['fecha'], dayfirst = True)
    df_sept = df_9.set_index('DATA')
    df_10['DATA'] = pd.to_datetime(df_10['fecha'], dayfirst = True)
    df_octo = df_10.set_index('DATA')
    df_11['DATA'] = pd.to_datetime(df_11['fecha'], dayfirst = True)
    df_nov = df_11.set_index('DATA')
    df_12['DATA'] = pd.to_datetime(df_12['fecha'], dayfirst = True)
    df_dec = df_12.set_index('DATA')
    
    frames = [df_gen,df_feb,df_mar,df_apr,df_may,df_jun,df_jul,df_aug,df_sept,df_octo,df_nov,df_dec]
    df_2021 = pd.concat(frames)
    #df_2021['tmed'].apply(lambda x: x.replace(',','.'))
    
    df_year = df_2021[['nombre','provincia','tmed','prec','tmin','horatmin','tmax','horatmax','dir','velmedia']]
    
    lleida = (df_year['nombre'] == 'LLEIDA') 
    manresa = (df_year['nombre'] == 'MANRESA')
    
    df_lleida = df_year.loc[lleida]
    df_manresa = df_year.loc[manresa]
    
      
    if city == 'lleida':
        return df_lleida

    if city == 'manresa':
        return df_manresa


def select_month(df,year,month):
    """
    separates the data frame into months
    'year' has to be between [2009,2022]
    'month' needs to be between 01-12 (0 before 1 to 9 needed)
    """
    return df.loc[year+'-'+month]


def select_day(df,year,month,day):
    """
    separates the data frame into days
    'day' has to be inside the range [01,31]
    """
    return df.loc[year+'-'+month+'-'+day]

def monthly_mean(city):
    """
    returns an array with the monthly mean values
    """
    means = data(city)['tmed'].resample('M').mean()
    return means


def maxmin(city, year, month, select):
    """
    resamples our data frame to find the daily max or min of a monthly data frame
    returns that extrem value as a float
    """
    if select == 'max':
        extrem = select_month(data(city),str(year),month)['tmax'].resample('D').max()
    if select == 'min':
        extrem = select_month(data(city),str(year),month)['tmin'].resample('D').min()
    
    return extrem.mean()

def extrems(city, year,select):
    """
    entering the city (lleida or manresa), a year and select ('max' or 'min')
    returns an array with the extrem monthly values
    """
    extrem_list = np.array([])
    for i in months_list:
        extrem_list = np.append(extrem_list,maxmin(city,year,i,select))
    return extrem_list


#%% TEMPERATURE GRAPHS
plt.style.use('ggplot')
plt.figure('Dades AEMET 2021')
plt.grid(True)
plt.title('2021')
plt.plot(months_names,monthly_mean('lleida'), label = 'TMm Lleida',linestyle = 'solid', marker = 'o', color = 'green')
plt.plot(months_names,extrems('lleida',2021,'max'), label = 'TXm Lleida',linestyle = 'solid', marker = 'o', color = 'darkgreen')
plt.plot(months_names,extrems('lleida',2021,'min'), label = 'TNm Leida',linestyle = 'solid', marker = 'o',color = 'lightgreen')
plt.plot(months_names,monthly_mean('manresa'),label = 'TMm Manresa',linestyle = 'solid', marker = 'o', color = 'red')
plt.plot(months_names,extrems('manresa',2021,'max'), label = 'TXm Manresa',linestyle = 'solid', marker = 'o', color = 'maroon')
plt.plot(months_names,extrems('manresa',2021,'min'), label = 'TNm Manresa',linestyle = 'solid', marker = 'o', color = 'lightcoral')
plt.legend(loc = 'best')
plt.ylabel('Temperature (°C)')
plt.tight_layout()
#plt.savefig('Dades AEMET 2021.png', format='png', dpi=800)

#%% WIND ROSES FOR JULY 2021 
from windrose import WindroseAxes
ws = select_month(data('manresa'),'2021','07')['velmedia']
wd = select_month(data('manresa'),'2021','07')['dir']
ax = WindroseAxes.from_ax()
ax.set_title('Manresa 07/21 UTC')
ax.bar(wd, ws, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')


#%% COMPARING LLEIDA, MANRESA, TÀRREGA AND MOLLERUSSA 
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
       

def meteocat_select_year(df,year):
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


def meteocat_select_month(df,year,month):
    """
    separates the data frame into months
    'year' has to be between [2009,2022]
    'month' needs to be between 01-12 (0 before 1 to 9 needed)
    """
    return df.loc[year+'-'+month]


def meteocat_select_day(df,year,month,day):
    """
    separates the data frame into days
    'day' has to be inside the range [01,31]
    """
    return df.loc[year+'-'+month+'-'+day]

def meteocat_monthly_mean(nomfitxer,year):
    """
    returns an array with the monthly mean values
    """
    means = meteocat_select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('M').mean()
    return means

def meteocat_maxmin(nomfitxer, year, month, select):
    """
    resamples our data frame to find the daily max or min of a monthly data frame
    returns that extrem value as a float
    """
    if select == 'max':
        extrem = meteocat_select_month(meteocat_select_year(read(nomfitxer),year),str(year),month)['VALOR_LECTURA'].resample('D').max()
    if select == 'min':
        extrem = meteocat_select_month(meteocat_select_year(read(nomfitxer),year),str(year),month)['VALOR_LECTURA'].resample('D').min()
    
    return extrem.mean()

def meteocat_extrems(nomfitxer,year,select):
    """
    returns a list of the extrem monthly values
    """
    extrem_list = np.array([])
    for i in months_list:
        extrem_list = np.append(extrem_list,meteocat_maxmin(nomfitxer,year,i,select))
    return extrem_list


plt.style.use('ggplot')
plt.figure('Dades 2021')
plt.grid(True)
plt.title('2021')
plt.plot(months_names,extrems('lleida',2021,'min'), label = 'Lleida',linestyle = 'solid', marker = 'o', color = 'green')
plt.plot(months_names,meteocat_extrems('XI_42.csv',2021,'min'), label = 'Mollerussa',linestyle = 'solid', marker = 'o', color = 'limegreen')
plt.plot(months_names,meteocat_extrems('C7_42.csv',2021,'min'), label = 'Tàrrega',linestyle = 'solid', marker = 'o', color = 'indianred')
plt.plot(months_names,extrems('manresa',2021,'min'),label = 'Manresa',linestyle = 'solid', marker = 'o', color = 'darkred')
plt.legend(loc = 'best')
plt.ylabel('Temperature (°C)')
plt.tight_layout()
#plt.savefig('TNm AEMET i SMC 2021.png', format='png', dpi=800)
