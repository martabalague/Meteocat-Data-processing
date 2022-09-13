#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:55:06 2022

@author: mbalague
"""
# LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_name = str(input('FILE NAME: '))
format_csv = '.csv'
months_names = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
months_list = ['01','02','03','04','05','06','07','08','09','10','11','12']

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

def preci(nomfitxer, year):
    """
    passing the file name and year of the station object of study 
    returns an array with the acumulated precipitation for each month of the year
    """
    acu = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('M').sum()
    return acu


def preci_1h(nomfitxer,year):
    """
    passing the file name (has to have 72 as the climatic constant code) and year of the station object of study 
    returns an array with the values of the maximum monthly precipitation registered in 1 hour
    """
    maxpre = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('M').max()
    return maxpre

def climatic_means(nomfitxer,selection):
    """
    passing a file name for each different station with 35 being the climatic constant code
    selection = 0 for accumulated precipitation, selection = 1 for maximum precipitation
    returns a numpy array with the means for the 2010-2019 interval
    """    
    means = np.array([])
    if selection == 0:
        a = preci(nomfitxer,2010)
        b = preci(nomfitxer,2011)
        c = preci(nomfitxer,2012)
        d = preci(nomfitxer,2013)
        e = preci(nomfitxer,2014)
        f = preci(nomfitxer,2015)
        g = preci(nomfitxer,2016)
        h = preci(nomfitxer,2017)
        j = preci(nomfitxer,2018)
        k = preci(nomfitxer,2019)
        
        for i in range(0,12):
            means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))
        
    if selection == 1:
        a = preci_1h(nomfitxer,2010)
        b = preci_1h(nomfitxer,2011)
        c = preci_1h(nomfitxer,2012)
        d = preci_1h(nomfitxer,2013)
        e = preci_1h(nomfitxer,2014)
        f = preci_1h(nomfitxer,2015)
        g = preci_1h(nomfitxer,2016)
        h = preci_1h(nomfitxer,2017)
        j = preci_1h(nomfitxer,2018)
        k = preci_1h(nomfitxer,2019)
        
        for i in range(0,12):
            means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))
    return means

#%% MONTHLY PRECIPITATION GRAPH FOR A SINGLE STATION
plt.style.use('ggplot')
plt.figure('Dades' + location + str(selected_year) + cc)
plt.grid(True)
plt.title(location)
plt.bar(months_names,preci(file_name,selected_year),color = 'forestgreen', label = selected_year)
plt.plot(months_names,climatic_means(file_name,0) ,'ko--',label = '2010-2019')
plt.ylabel('Monthly precipitacion (mm)')
plt.ylim(0,70) #can be adjusted
plt.legend(loc = 1)
#plt.savefig('Dades'+location+str(selected_year)+cc+'.png', format='png', dpi=800)  
plt.tight_layout()

#%% MONTHLY MAX PRECIPITATION IN 1 HOUR GRAPH FOR A SINGLE STATION
plt.style.use('ggplot')
plt.figure('Dades' + location + str(selected_year) + cc)
plt.grid(True)
plt.title(location)
plt.bar(months_names,preci_1h(file_name,selected_year),color = 'maroon', label = selected_year)
plt.plot(months_names,climatic_means(file_name,1) ,'ko--',label = '2010-2019')
plt.ylabel('Max 1h Monthly precipitacion (mm)')
plt.ylim(0,4) #can be adjusted
plt.legend(loc = 1)
#plt.savefig('Dades'+location+str(selected_year)+cc+'.png', format='png', dpi=800)  
plt.tight_layout()

#%% PRECIPITATION BOXPLOTS 
def dfbp(nomfitxer):
    """
    takes the monthly data from each year and generates a new data frame with a column indicating the month 
    and the acumulated precipitation for that month
    """
    a = preci(nomfitxer,2010)
    b = preci(nomfitxer,2011)
    c = preci(nomfitxer,2012)
    d = preci(nomfitxer,2013)
    e = preci(nomfitxer,2014)
    f = preci(nomfitxer,2015)
    g = preci(nomfitxer,2016)
    h = preci(nomfitxer,2017)
    j = preci(nomfitxer,2018)
    k = preci(nomfitxer,2019)
    
    gen = [a[0],b[0],c[0],d[0],e[0],f[0],g[0],h[0],j[0],k[0]]
    feb = [a[1],b[1],c[1],d[1],e[1],f[1],g[1],h[1],j[1],k[1]]
    mar = [a[2],b[2],c[2],d[2],e[2],f[2],g[2],h[2],j[2],k[2]] 
    apr = [a[3],b[3],c[3],d[3],e[3],f[3],g[3],h[3],j[3],k[3]]
    may = [a[4],b[4],c[4],d[4],e[4],f[4],g[4],h[4],j[4],k[4]]
    jun = [a[5],b[5],c[5],d[5],e[5],f[5],g[5],h[5],j[5],k[5]]
    jul = [a[6],b[6],c[6],d[6],e[6],f[6],g[6],h[6],j[6],k[6]]
    aug = [a[7],b[7],c[7],d[7],e[7],f[7],g[7],h[7],j[7],k[7]]
    sept = [a[8],b[8],c[8],d[8],e[8],f[8],g[8],h[8],j[8],k[8]]
    octo = [a[9],b[9],c[9],d[9],e[9],f[9],g[9],h[9],j[9],k[9]]
    nov = [a[10],b[10],c[10],d[10],e[10],f[10],g[10],h[10],j[10],k[10]]
    dec = [a[11],b[11],c[11],d[11],e[11],f[11],g[11],h[11],j[11],k[11]]
        
    x = [1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12]   
    y = gen+feb+mar+apr+may+jun+jul+aug+sept+octo+nov+dec   
        
    df = pd.DataFrame(list(zip(x, y)), columns =['Month', 'ACU'])
    return df

ax = dfbp('XI_35.csv').boxplot(column=['ACU'], by = 'Month', grid = False, showmeans = True, meanline = True) 
#THE DASHED LINE INDICATES THE MONTHLY MEAN WHILE THE SOLID ONE INDICATES THE MEDIAN
plt.suptitle("")
ax.plot([1,2,3,4,5,6,7,8,9,10,11,12], preci('XI_35.csv',2021),'ro', label = '2021')
ax.set_xlabel("Months")
ax.set_ylim(-5,150)
ax.set_title('PPT Mollerussa 2010-2019')
ax.set_ylabel("Precipitation (mm)")
ax.set_xticks(np.arange(13))
ax.legend(loc = 'best')

#%% MONTHLY PRECIPITATION GRAPH COMPARING ALL STATIONS
r = np.arange(12)
width = 0.11
plt.style.use('ggplot')
plt.grid(True)
  
 
plt.bar(r, preci('WL_35.csv',2021), color = 'lightcoral',
        width = width, edgecolor = None,
        label='Sant Martí de Riucorb')  

plt.bar(r+width, preci('C7_35.csv',2021), color = 'indianred',
        width = width, edgecolor = None,
        label='Tàrrega') 

plt.bar(r+2*width, preci('VD_35.csv',2021), color = 'firebrick',
        width = width, edgecolor = None,
        label='El Canós')  
plt.bar(r+3*width, preci('C8_35.csv',2021), color = 'maroon',
        width = width, edgecolor = None,
        label='Cervera')  
        
plt.bar(r+4*width, preci('V8_35.csv',2021), color = 'lightgreen',
        width = width, edgecolor = None,
        label='El Poal')

plt.bar(r+5*width, preci('XI_35.csv',2021), color = 'limegreen',
        width = width, edgecolor = None,
        label='Mollerussa')

plt.bar(r+6*width, preci('WC_35.csv',2021), color = 'seagreen',
        width = width, edgecolor = None,
        label='Golmés')

plt.bar(r+7*width, preci('C6_35.csv',2021), color = 'darkgreen',
        width = width, edgecolor = None,
        label='Castellnou de Seana')


plt.ylabel("Monthly precipitation (mm)")
plt.title("2021")
  
plt.grid(True)
plt.ylim(0,70)
plt.xticks(r +width,months_names)
plt.legend(loc = 7)

#%% PRECIPITATION GRAPH COMPARING 2 STATIONS 
r = np.arange(12)
width = 0.30
plt.grid(True)
plt.style.use('ggplot')
  
plt.bar(r, preci('C7_35.csv',2021), color = 'brown',
        width = width, edgecolor = None,
        label='Tàrrega')  
plt.bar(r+width, preci('XI_35.csv',2021), color = 'green',
        width = width, edgecolor = None,
        label='Mollerussa')

plt.ylabel("Monthly precipitation (mm)")
plt.title("2021")
plt.grid(True)
plt.ylim(0,70)
plt.xticks(r + width/2,months_names)
#plt.savefig('Comparativa Tàrrega/Castellnou de Seana'+ str(selected_year) + '.png', format='png', dpi=400)
plt.legend(loc = 1)
