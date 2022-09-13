#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:25:56 2022

@author: mbalague
"""
# LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_name = str(input('FILE NAME: '))
format_csv = '.csv'
months_names = ['May','June','July','Aug','Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr']
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

def monthly_mean(nomfitxer,year):
    """
    returns an array with the monthly mean values
    """
    means = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('M').mean()
    return means

def maxmin(nomfitxer, year, month, select):
    """
    resamples our data frame to find the daily max or min of a monthly data frame
    returns that extrem value as a float
    """
    if select == 'max':
        extrem = select_month(select_year(read(nomfitxer),year),str(year),month)['VALOR_LECTURA'].resample('D').max()
    if select == 'min':
        extrem = select_month(select_year(read(nomfitxer),year),str(year),month)['VALOR_LECTURA'].resample('D').min()
    
    return extrem.mean()

def extrems(nomfitxer,year,select):
    """
    function that gets the values depending if the selected year is 2022 or not (if it is, then it only adds to the list the values for january-april)
    returns a list of the extrem values
    """
    extrem_list = np.array([])
    if year != 2022:
        for i in months_list:
            extrem_list = np.append(extrem_list,maxmin(nomfitxer,year,i,select))
    else:
        for j in ['01','02','03','04']:
             extrem_list = np.append(extrem_list,maxmin(nomfitxer,year,j,select))
        
    return extrem_list

def preci(nomfitxer,year):
    """
    passing the file name and year of the station object of study 
    returns an array with the acumulated precipitation for each month of the year
    """
    acu = select_year(read(nomfitxer),year)['VALOR_LECTURA'].resample('M').sum()
    return acu

def climatic_means(nomfitxer,selection):
    """
    Parameters
    ----------
    nomfitxer
    selection : 0 for mean temperature, 1 for max temperature, 2 for min temperature, 3 for precipitation
    select = 'max' o 'min'
    Returns
    -------
    mean : means array (adapted to fit MAY 2021 - APRIL 2022)

    """    
    means = np.array([])
    if selection == 0:
        a = monthly_mean(nomfitxer,2010)
        b = monthly_mean(nomfitxer,2011)
        c = monthly_mean(nomfitxer,2012)
        d = monthly_mean(nomfitxer,2013)
        e = monthly_mean(nomfitxer,2014)
        f = monthly_mean(nomfitxer,2015)
        g = monthly_mean(nomfitxer,2016)
        h = monthly_mean(nomfitxer,2017)
        j = monthly_mean(nomfitxer,2018)
        k = monthly_mean(nomfitxer,2019)
        
        gen = (a[0]+b[0]+c[0]+d[0]+e[0]+f[0]+g[0]+h[0]+j[0]+k[0])/10
        feb = (a[1]+b[1]+c[1]+d[1]+e[1]+f[1]+g[1]+h[1]+j[1]+k[1])/10
        mar = (a[2]+b[2]+c[2]+d[2]+e[2]+f[2]+g[2]+h[2]+j[2]+k[2])/10
        apr = (a[3]+b[3]+c[3]+d[3]+e[3]+f[3]+g[3]+h[3]+j[3]+k[3])/10
        mai = (a[4]+b[4]+c[4]+d[4]+e[4]+f[4]+g[4]+h[4]+j[4]+k[4])/10
        jun = (a[5]+b[5]+c[5]+d[5]+e[5]+f[5]+g[5]+h[5]+j[5]+k[5])/10
        jul = (a[6]+b[6]+c[6]+d[6]+e[6]+f[6]+g[6]+h[6]+j[6]+k[6])/10
        ago = (a[7]+b[7]+c[7]+d[7]+e[7]+f[7]+g[7]+h[7]+j[7]+k[7])/10
        sept = (a[8]+b[8]+c[8]+d[8]+e[8]+f[8]+g[8]+h[8]+j[8]+k[8])/10
        octo = (a[9]+b[9]+c[9]+d[9]+e[9]+f[9]+g[9]+h[9]+j[9]+k[9])/10
        nov = (a[10]+b[10]+c[10]+d[10]+e[10]+f[10]+g[10]+h[10]+j[10]+k[10])/10
        dec = (a[11]+b[11]+c[11]+d[11]+e[11]+f[11]+g[11]+h[11]+j[11]+k[11])/10
        means = np.append(means,(mai,jun,jul,ago,sept,octo,nov,dec,gen,feb,mar,apr))

        
    if selection == 1:
        a = extrems(nomfitxer,2010,'max')
        b = extrems(nomfitxer,2011,'max')
        c = extrems(nomfitxer,2012,'max')
        d = extrems(nomfitxer,2013,'max')
        e = extrems(nomfitxer,2014,'max')
        f = extrems(nomfitxer,2015,'max')
        g = extrems(nomfitxer,2016,'max')
        h = extrems(nomfitxer,2017,'max')
        j = extrems(nomfitxer,2018,'max')
        k = extrems(nomfitxer,2019,'max')
            
        gen = (a[0]+b[0]+c[0]+d[0]+e[0]+f[0]+g[0]+h[0]+j[0]+k[0])/10
        feb = (a[1]+b[1]+c[1]+d[1]+e[1]+f[1]+g[1]+h[1]+j[1]+k[1])/10
        mar = (a[2]+b[2]+c[2]+d[2]+e[2]+f[2]+g[2]+h[2]+j[2]+k[2])/10
        apr = (a[3]+b[3]+c[3]+d[3]+e[3]+f[3]+g[3]+h[3]+j[3]+k[3])/10
        mai = (a[4]+b[4]+c[4]+d[4]+e[4]+f[4]+g[4]+h[4]+j[4]+k[4])/10
        jun = (a[5]+b[5]+c[5]+d[5]+e[5]+f[5]+g[5]+h[5]+j[5]+k[5])/10
        jul = (a[6]+b[6]+c[6]+d[6]+e[6]+f[6]+g[6]+h[6]+j[6]+k[6])/10
        ago = (a[7]+b[7]+c[7]+d[7]+e[7]+f[7]+g[7]+h[7]+j[7]+k[7])/10
        sept = (a[8]+b[8]+c[8]+d[8]+e[8]+f[8]+g[8]+h[8]+j[8]+k[8])/10
        octo = (a[9]+b[9]+c[9]+d[9]+e[9]+f[9]+g[9]+h[9]+j[9]+k[9])/10
        nov = (a[10]+b[10]+c[10]+d[10]+e[10]+f[10]+g[10]+h[10]+j[10]+k[10])/10
        dec = (a[11]+b[11]+c[11]+d[11]+e[11]+f[11]+g[11]+h[11]+j[11]+k[11])/10
        means = np.append(means,(mai,jun,jul,ago,sept,octo,nov,dec,gen,feb,mar,apr))
               
        
    if selection == 2:
        a = extrems(nomfitxer,2010,'min')
        b = extrems(nomfitxer,2011,'min')
        c = extrems(nomfitxer,2012,'min')
        d = extrems(nomfitxer,2013,'min')
        e = extrems(nomfitxer,2014,'min')
        f = extrems(nomfitxer,2015,'min')
        g = extrems(nomfitxer,2016,'min')
        h = extrems(nomfitxer,2017,'min')
        j = extrems(nomfitxer,2018,'min')
        k = extrems(nomfitxer,2019,'min')
        
        gen = (a[0]+b[0]+c[0]+d[0]+e[0]+f[0]+g[0]+h[0]+j[0]+k[0])/10
        feb = (a[1]+b[1]+c[1]+d[1]+e[1]+f[1]+g[1]+h[1]+j[1]+k[1])/10
        mar = (a[2]+b[2]+c[2]+d[2]+e[2]+f[2]+g[2]+h[2]+j[2]+k[2])/10
        apr = (a[3]+b[3]+c[3]+d[3]+e[3]+f[3]+g[3]+h[3]+j[3]+k[3])/10
        mai = (a[4]+b[4]+c[4]+d[4]+e[4]+f[4]+g[4]+h[4]+j[4]+k[4])/10
        jun = (a[5]+b[5]+c[5]+d[5]+e[5]+f[5]+g[5]+h[5]+j[5]+k[5])/10
        jul = (a[6]+b[6]+c[6]+d[6]+e[6]+f[6]+g[6]+h[6]+j[6]+k[6])/10
        ago = (a[7]+b[7]+c[7]+d[7]+e[7]+f[7]+g[7]+h[7]+j[7]+k[7])/10
        sept = (a[8]+b[8]+c[8]+d[8]+e[8]+f[8]+g[8]+h[8]+j[8]+k[8])/10
        octo = (a[9]+b[9]+c[9]+d[9]+e[9]+f[9]+g[9]+h[9]+j[9]+k[9])/10
        nov = (a[10]+b[10]+c[10]+d[10]+e[10]+f[10]+g[10]+h[10]+j[10]+k[10])/10
        dec = (a[11]+b[11]+c[11]+d[11]+e[11]+f[11]+g[11]+h[11]+j[11]+k[11])/10
        means = np.append(means,(mai,jun,jul,ago,sept,octo,nov,dec,gen,feb,mar,apr))
        
    if selection == 3: #we add the option of the mean accumulated precipitation
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
        
        gen = (a[0]+b[0]+c[0]+d[0]+e[0]+f[0]+g[0]+h[0]+j[0]+k[0])/10
        feb = (a[1]+b[1]+c[1]+d[1]+e[1]+f[1]+g[1]+h[1]+j[1]+k[1])/10
        mar = (a[2]+b[2]+c[2]+d[2]+e[2]+f[2]+g[2]+h[2]+j[2]+k[2])/10
        apr = (a[3]+b[3]+c[3]+d[3]+e[3]+f[3]+g[3]+h[3]+j[3]+k[3])/10
        mai = (a[4]+b[4]+c[4]+d[4]+e[4]+f[4]+g[4]+h[4]+j[4]+k[4])/10
        jun = (a[5]+b[5]+c[5]+d[5]+e[5]+f[5]+g[5]+h[5]+j[5]+k[5])/10
        jul = (a[6]+b[6]+c[6]+d[6]+e[6]+f[6]+g[6]+h[6]+j[6]+k[6])/10
        ago = (a[7]+b[7]+c[7]+d[7]+e[7]+f[7]+g[7]+h[7]+j[7]+k[7])/10
        sept = (a[8]+b[8]+c[8]+d[8]+e[8]+f[8]+g[8]+h[8]+j[8]+k[8])/10
        octo = (a[9]+b[9]+c[9]+d[9]+e[9]+f[9]+g[9]+h[9]+j[9]+k[9])/10
        nov = (a[10]+b[10]+c[10]+d[10]+e[10]+f[10]+g[10]+h[10]+j[10]+k[10])/10
        dec = (a[11]+b[11]+c[11]+d[11]+e[11]+f[11]+g[11]+h[11]+j[11]+k[11])/10
        means = np.append(means,(mai,jun,jul,ago,sept,octo,nov,dec,gen,feb,mar,apr))
    
    return means

def campanya(nomfitxer,select):
    """
    To get a range of months, we add to mitjanes the values taking into account the month (0: january, 11:december)
    returns an array with the mean values for the wanted meteorological variable 
    """
    if select == 0:
        a = monthly_mean(nomfitxer,2021) 
        b = monthly_mean(nomfitxer,2022)
        mitjanes = np.array([])
        mitjanes = np.append(mitjanes,(a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],b[0],b[1],b[2],b[3])) 
        
    if select == 1:
        c = extrems(nomfitxer, 2021,'max')
        d = extrems(nomfitxer, 2022,'max')
        mitjanes = np.array([])
        mitjanes = np.append(mitjanes, (c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],d[0],d[1],d[2],d[3]))
        
    if select ==2:
        e = extrems(nomfitxer, 2021, 'min')
        f = extrems(nomfitxer, 2022, 'min')
        mitjanes = np.array([])
        mitjanes = np.append(mitjanes, (e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11],f[0],f[1],f[2],f[3]))

    if select ==3:
       g = preci(nomfitxer,2021) 
       h = preci(nomfitxer,2022)
       mitjanes = np.array([])
       mitjanes = np.append(mitjanes,(g[4],g[5],g[6],g[7],g[8],g[9],g[10],g[11],h[0],h[1],h[2],h[3])) 
        
    return mitjanes

#%% TEMPERATURE PLOTS 21-22 FOR A SINGLE STATION
plt.figure('Temperatures 21-22' + location)
plt.grid(True)
plt.style.use('ggplot')
plt.title(location)
plt.plot(months_names,campanya('C7_32.csv',0),label = 'TMm 2021',linestyle = 'solid', marker = 'o', color = 'indianred')
plt.plot(months_names,climatic_means(file_name,0), label = 'TMm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'indianred')
plt.plot(months_names,campanya('C7_40.csv',1), label = 'TXm 2021',linestyle = 'solid', marker = 'o', color = 'maroon')
plt.plot(months_names,climatic_means('C7_40.csv',1),label = 'TXm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'maroon')
plt.plot(months_names,campanya('C7_42.csv',2), label = 'TNm 2021',linestyle = 'solid', marker = 'o', color = 'lightcoral')
plt.plot(months_names,climatic_means('C7_42.csv',2),label = 'TNm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'lightcoral')
plt.legend(loc = 1)
plt.ylabel('Temperature (°C)')
plt.tight_layout()

#%% PRECIPITATION BARS 21-22 FOR A SINGLE STATION
plt.style.use('ggplot')
plt.figure('Precipitació 21-22' + location)
plt.grid(True)
plt.title(location)
plt.bar(months_names,campanya('C7_35.csv',3), color = 'maroon', label = '2021-2022')
plt.plot(months_names,climatic_means(file_name,3) ,'ko--',label = '2010-2019')
plt.ylim(0,70)
plt.ylabel('Monthly precipitacion (mm)')
plt.legend(loc = 1)
plt.tight_layout()

#%% TEMPERATURE COMPARISON FOR 2 STATIONS
plt.figure('Temperatures 21-22' + location)
plt.grid(True)
plt.style.use('ggplot')
plt.title('Temperatures 21-22')
plt.plot(months_names,campanya('C7_32.csv',0),label = 'TMm Tàrrega',linestyle = 'solid', marker = 'o', color = 'indianred')
plt.plot(months_names,campanya('C7_40.csv',1),label = 'TXm Tàrrega',linestyle = 'solid', marker = 'o', color = 'maroon')
plt.plot(months_names,campanya('C7_42.csv',2), label = 'TNm Tàrrega',linestyle = 'solid', marker = 'o', color = 'lightcoral')
plt.plot(months_names,campanya('XI_32.csv',0),label = 'TMm Mollerussa',linestyle = 'solid', marker = 'o', color = 'limegreen')
plt.plot(months_names,campanya('XI_40.csv',1), label = 'TXm Mollerussa',linestyle = 'solid', marker = 'o', color = 'darkgreen')
plt.plot(months_names,campanya('XI_42.csv',2),label = 'TNm Mollerussa',linestyle = 'solid', marker = 'o', color = 'lightgreen')
plt.legend(loc = 1)
plt.ylabel('Temperature (°C)')
plt.tight_layout()

#%% MEAN TEMPERATURE COMPARISON 21-22 FOR ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp 21-22')
plt.grid(True)
plt.title('TMm 21-22')
plt.plot(months_names, campanya('WL_32.csv',0), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, campanya('C7_32.csv',0),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, campanya('VD_32.csv',0),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, campanya('C8_32.csv',0),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, campanya('V8_32.csv',0),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, campanya('XI_32.csv',0), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, campanya('WC_32.csv',0),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, campanya('C6_32.csv',0),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (°C)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp.png', format='png', dpi=800)

#%% MAX TEMPERATURE COMPARISON 21-22 FOR ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp Max 21-22')
plt.grid(True)
plt.title('TXm 21-22')
plt.plot(months_names, campanya('WL_40.csv',1), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, campanya('C7_40.csv',1),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, campanya('VD_40.csv',1),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, campanya('C8_40.csv',1),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, campanya('V8_40.csv',1),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, campanya('XI_40.csv',1), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, campanya('WC_40.csv',1),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, campanya('C6_40.csv',1),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (°C)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp Max.png', format='png', dpi=800)

#%% MIN TEMPERATURE COMPARISON 21-22 FOR ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp Min 21-22')
plt.grid(True)
plt.title('TNm 21-22')
plt.plot(months_names, campanya('WL_42.csv',2), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, campanya('C7_42.csv',2),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, campanya('VD_42.csv',2),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, campanya('C8_42.csv',2),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, campanya('V8_42.csv',2),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, campanya('XI_42.csv',2), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, campanya('WC_42.csv',2),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, campanya('C6_42.csv',2),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (°C)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp Max.png', format='png', dpi=800)