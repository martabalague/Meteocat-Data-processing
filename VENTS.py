#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:07:10 2022

@author: mbalague
"""
# LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
format_csv = '.csv'

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



# EXAMPLE OF THE FORMAT USED TO OBTAIN THE DATA FRAME WITH THE DAILY VALUES
# DATA = select_day(select_month(select_year(read('C7_31.csv'),2021),'2021','07'), '2021','07','01')

        
        
#%% DAILY WIND DIRECTION GRAPH
plt.figure('Dades 01 07 2021')

plt.subplot(211)
plt.title('Tàrrega')
plt.style.use('ggplot')
plt.grid(True)
plt.plot(select_day(select_month(select_year(read('C7_31.csv'),2021),'2021','07'), '2021','07','01')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C7_31.csv'),2021),'2021','07'), '2021','07','01')['VALOR_LECTURA'],'ro')
plt.ylim(0,360)
plt.xlabel('UTC')
plt.ylabel('DV (º)')


plt.subplot(212)
plt.title('Castellnou de Seana')
plt.style.use('ggplot')
plt.grid(True)
plt.plot(select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07','01')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07','01')['VALOR_LECTURA'],'go')
plt.ylim(0,360)
plt.xlabel('UTC')
plt.ylabel('DV (º)')
plt.tight_layout()
    

#%% DAILY WIND SPEED, DIRECTION AND MEAN TEMPERATURE FOR 2 STATIONS
fig = plt.figure()
host = fig.add_subplot(211)

par1 = host.twinx()
par2 = host.twinx()
    
host.set_ylim(0, 360)
par1.set_ylim(0, 40)
par2.set_ylim(0, 16)
    
host.set_xlabel("UTC")
host.set_ylabel("Wind Direction (º)")
par1.set_ylabel("Max Temperature (ºC)")
par2.set_ylabel("Velocity (m/s)")

p1, = host.plot(select_day(select_month(select_year(read('C7_31.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C7_31.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "ro", label="Wind Direction")
p2, = par1.plot(select_day(select_month(select_year(read('C7_40.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C7_32.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "b-", label="Max Temperature")
p3, = par2.plot(select_day(select_month(select_year(read('C7_30.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C7_30.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "k-", label="Velocity")

lns = [p1, p2, p3]
host.legend(handles=lns, loc='best')
par2.spines['right'].set_position(('outward', 60))
  
host = fig.add_subplot(212)

par1 = host.twinx()
par2 = host.twinx()
    
host.set_ylim(0, 360)
par1.set_ylim(0, 40)
par2.set_ylim(0, 16)
    
host.set_xlabel("UTC")
host.set_ylabel("Wind Direction (º)")
par1.set_ylabel("Max Temperature (ºC)")
par2.set_ylabel("Velocity (m/s)")

p1, = host.plot(select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "go", label="Wind Direction")
p2, = par1.plot(select_day(select_month(select_year(read('C6_40.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C6_32.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "b-", label="Max Temperature")
p3, = par2.plot(select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'].keys(), select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07','07')['VALOR_LECTURA'], "k-", label="Velocity")

lns = [p1, p2, p3]
host.legend(handles=lns, loc='best')
par2.spines['right'].set_position(('outward', 60))
fig.tight_layout()

#%% 3-HOURLY DAILY WIND ROSE (00-03)
from windrose import WindroseAxes
dia = str(input('DIA:'))
ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('00:00','03:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('00:00','03:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 00-03h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (03-06)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('03:00','06:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('03:00','06:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 03-06h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N','NW','W','SW','S','SE','E','NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (06-09)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('06:00','09:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('06:00','09:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 06-09h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (09-12)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('09:00','12:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('09:00','12:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 09-12h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (12-15)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('12:00','15:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('12:00','15:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 12-15h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (15-18)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('15:00','18:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('15:00','18:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 15-18h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (18-21)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('18:00','21:00')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('18:00','21:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 18-21h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY DAILY WIND ROSE (21-23:30)
from windrose import WindroseAxes

ws = select_day(select_month(select_year(read('C6_30.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
ws_hour = ws.between_time('21:00','23:30')
wd = select_day(select_month(select_year(read('C6_31.csv'),2021),'2021','07'), '2021','07',dia)['VALOR_LECTURA']
wd_hour = wd.between_time('21:00','23:30')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana '+dia+'/07/21 21-00h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (00-03)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('00:00','03:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('00:00','03:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 00-03h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (03-06)
from windrose import WindroseAxes
ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('03:00','06:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('03:00','06:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 03-06h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (06-09)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('06:00','09:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('06:00','09:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 06-09h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (09-12)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('09:00','12:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('09:00','12:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 09-12h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (12-15)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('12:00','15:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('12:00','15:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 12-15h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (15-18)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('15:00','18:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('15:00','18:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 15-18h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (18-21)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('18:00','21:00')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('18:00','21:00')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 18-21h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')

#%% 3-HOURLY MONTHLY MEAN WIND ROSES (21-23:30)
from windrose import WindroseAxes

ws = select_month(select_year(read('C6_30.csv'),2021),'2021','07')['VALOR_LECTURA']
ws_hour = ws.between_time('21:00','23:30')
wd = select_month(select_year(read('C6_31.csv'),2021),'2021','07')['VALOR_LECTURA']
wd_hour = wd.between_time('21:00','23:30')
ax = WindroseAxes.from_ax()
ax.set_title('Castellnou de Seana 07/21 21-00h UTC')
ax.bar(wd_hour, ws_hour, bins = np.arange(0, 15, 1.5))
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
ax.set_legend(loc = 'lower left')
