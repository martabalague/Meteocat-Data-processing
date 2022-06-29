#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:40:11 2022

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
    returns a list of the extrem monthly values
    """
    extrem_list = np.array([])
    for i in months_list:
        extrem_list = np.append(extrem_list,maxmin(nomfitxer,year,i,select))
    return extrem_list

def climatic_means(nomfitxer,selection):
    """
    Parameters
    ----------
    nomfitxer
    selection : 0 -> mean temperature, 1 -> max temperature, 2 -> min temperature
    select = 'max' o 'min'
    Returns
    -------
    mean : array with the monthly mean

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
        
        for i in range(0,12):
            means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))

        
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
            
        for i in range(0,12):
            means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))
               
        
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
        
        for i in range(0,12):
            means = np.append(means,((a[i]+b[i]+c[i]+d[i]+e[i]+f[i]+g[i]+h[i]+j[i]+k[i])/10))
    return means


#%% BOXPLOT TMm 

def dfbp(nomfitxer):
    """
    gets the yearly data and generates a new data frame with an added column showing the month 
    """
    df = read(nomfitxer)
    filt = (df['DATA'] >= pd.to_datetime('2010-01-01')) & (df['DATA'] < pd.to_datetime('2020-01-01'))
    df_year = df.loc[filt]
    df_year = df_year.sort_values('DATA',ascending = True)
    df_year['Month'] = df_year['DATA'].dt.month
    
    df_final = df_year[['VALOR_LECTURA','Month']]
    return df_final


ax = dfbp('XI_32.csv').boxplot(column=['VALOR_LECTURA'], by ='Month', grid = False, showmeans = True, meanline = True)
plt.suptitle("")
ax.plot([1,2,3,4,5,6,7,8,9,10,11,12], monthly_mean('C8_32.csv',2021),'ro', label = '2021')
ax.set_xlabel("Months")
ax.set_title('TMm Mollerussa 2010-2019')
ax.set_ylabel("Temperature (ºC)")
ax.set_xticks(np.arange(13))
ax.legend(loc = 'best')


#%% BOXPLOTS TXm & TNm

def dfbp(nomfitxer,selection):
    """
    gets the yearly data and generates a new data frame with an added column showing the month 
    """
    df = read(nomfitxer)
    filt = (df['DATA'] >= pd.to_datetime('2010-01-01')) & (df['DATA'] < pd.to_datetime('2020-01-01'))
    df_years = df.loc[filt]
    df_years = df_years.sort_values('DATA',ascending = True)
    df_years['MONTH'] = df_years['DATA'].dt.month
    
    
    a = extrems(nomfitxer,2010,selection)
    b = extrems(nomfitxer,2011,selection)
    c = extrems(nomfitxer,2012,selection)
    d = extrems(nomfitxer,2013,selection)
    e = extrems(nomfitxer,2014,selection)
    f = extrems(nomfitxer,2015,selection)
    g = extrems(nomfitxer,2016,selection)
    h = extrems(nomfitxer,2017,selection)
    j = extrems(nomfitxer,2018,selection)
    k = extrems(nomfitxer,2019,selection)
    
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
        
   
    df_final = pd.DataFrame(list(zip(x, y)), columns =['MONTH', 'EXTREM'])
    return df_final

ax = dfbp('WL_42.csv','min').boxplot(column=['EXTREM'], by ='MONTH', grid = False, showmeans = True, meanline = True)
plt.suptitle("")
ax.plot([1,2,3,4,5,6,7,8,9,10,11,12],extrems('WL_42.csv',2021,'min'),'ro', label = '2021')
ax.set_xlabel("Months")
ax.set_title('TNm Sant Martí de Riucorb 2010-2019')
ax.set_ylabel("Temperature (ºC)")
ax.set_xticks(np.arange(13))
ax.legend(loc = 'best')

#%% TEMPERATURE COMPARISON BETWEEN TÀRREGA & MOLLERUSSA
plt.style.use('ggplot')

plt.figure(1)
plt.grid(True)
plt.title('2021')

plt.plot(months_names,monthly_mean('XI_32.csv',2021), label = 'TMm Mollerussa',linestyle = 'solid', marker = 'o', color = 'green')
plt.plot(months_names,extrems('XI_40.csv',2021,'max'), label = 'TXm Mollerussa',linestyle = 'solid', marker = 'o', color = 'darkgreen')
plt.plot(months_names,extrems('XI_42.csv',2021,'min'), label = 'TNm Mollerussa',linestyle = 'solid', marker = 'o',color = 'lightgreen')
plt.plot(months_names,monthly_mean('C7_32.csv',2021),label = 'TMm Tàrrega',linestyle = 'solid', marker = 'o', color = 'red')
plt.plot(months_names,extrems('C7_40.csv',2021,'max'), label = 'TXm Tàrrega',linestyle = 'solid', marker = 'o', color = 'maroon')
plt.plot(months_names,extrems('C7_42.csv',2021,'min'), label = 'TNm Tàrrega',linestyle = 'solid', marker = 'o', color = 'lightcoral')
plt.legend(loc = 'best')
plt.ylabel('Temperature (ºC)')
plt.tight_layout()

#plt.savefig('Mollerusa i Tàrrega 2021.png', format='png', dpi=800)

#%% TEMPERATURE GRAPH FOR A SINGLE STATION
plt.style.use('ggplot')

plt.figure('Dades ' + location + str(selected_year))
plt.grid(True)
plt.title(location)

plt.plot(months_names,monthly_mean(file_name,selected_year), label = 'TMm '+str(selected_year),linestyle = 'solid', marker = 'o', color = 'seagreen')
plt.plot(months_names,climatic_means(file_name,0),label = 'TMm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'seagreen' )
plt.plot(months_names,extrems('V8_40.csv',2021,'max'), label = 'TXm '+str(selected_year),linestyle = 'solid', marker = 'o', color = 'darkgreen')
plt.plot(months_names,climatic_means('V8_40.csv',1),label = 'TXm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'darkgreen')
plt.plot(months_names,extrems('V8_42.csv',2021,'min'), label = 'TNm '+str(selected_year),linestyle = 'solid', marker = 'o', color = 'lightgreen')
plt.plot(months_names,climatic_means('V8_42.csv',2),label = 'TNm 2010-2019',linestyle = 'dashed', marker = 'o', color = 'lightgreen')
plt.legend(loc = 8)
plt.ylabel('Temperature (ºC)')
plt.tight_layout()

#plt.savefig('Comparativa Temp El Poal.png', format='png', dpi=800)

#%% TEMPERATURE COMPARISON FOR 2021 ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp')
plt.grid(True)
plt.title('TMm 2021')
plt.plot(months_names, monthly_mean('WL_32.csv',2021), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, monthly_mean('C7_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, monthly_mean('VD_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, monthly_mean('C8_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, monthly_mean('V8_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, monthly_mean('XI_32.csv',2021), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, monthly_mean('WC_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, monthly_mean('C6_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp.png', format='png', dpi=800)
#%% MAX TEMPERATURE COMPARISON FOR 2021 ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp Max')
plt.grid(True)
plt.title('TXm 2021')
plt.plot(months_names, extrems('WL_40.csv',2021,'max'), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, extrems('C7_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, extrems('VD_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, extrems('C8_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, extrems('V8_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, extrems('XI_40.csv',2021,'max'), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, extrems('WC_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, extrems('C6_40.csv',2021,'max'),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp Max.png', format='png', dpi=800)
#%% MIN TEMPERATURE COMPARISON FOR 2021 ALL STATIONS
plt.style.use('ggplot')
plt.figure('Comparativa Temp Min')
plt.grid(True)
plt.title('TNm 2021')
plt.plot(months_names, extrems('WL_42.csv',2021,'min'), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, extrems('C7_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, extrems('VD_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, extrems('C8_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, extrems('V8_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, extrems('XI_42.csv',2021,'min'), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, extrems('WC_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, extrems('C6_42.csv',2021,'min'),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')
plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
#plt.ylim(5,35) #can be adjusted
plt.tight_layout()
#plt.savefig('Comparativa Temp Min.png', format='png', dpi=800)

#%% MAX TEMPERATURE COMPARISON 2010-2019
plt.style.use('ggplot')
plt.figure('Comparativa TXm')
plt.grid(True)
plt.title('TNm 2010-19')
plt.plot(months_names, climatic_means('WL_40.csv',1), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, climatic_means('C7_40.csv',1),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, climatic_means('VD_40.csv',1),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, climatic_means('C8_40.csv',1),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, climatic_means('V8_40.csv',1),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, climatic_means('XI_40.csv',1), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, climatic_means('WC_40.csv',1),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, climatic_means('C6_40.csv',1),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')


plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
plt.tight_layout()
#plt.savefig('Comparativa TXm.png', format='png', dpi=800)
#%% MIN TEMPERATURE COMPARISON 2010-2019
plt.style.use('ggplot')
plt.figure('Comparativa TNm')
plt.grid(True)
plt.title('TNm 2010-19')
plt.plot(months_names, climatic_means('WL_42.csv',2), linestyle = 'solid', marker = 'o', color = 'lightcoral', label='Sant Martí de Riucorb')  
plt.plot(months_names, climatic_means('C7_42.csv',2),linestyle = 'solid', marker = 'o', color = 'indianred', label='Tàrrega') 
plt.plot(months_names, climatic_means('VD_42.csv',2),linestyle = 'solid', marker = 'o', color = 'firebrick', label='El Canós')  
plt.plot(months_names, climatic_means('C8_42.csv',2),linestyle = 'solid', marker = 'o', color = 'maroon', label='Cervera')  
plt.plot(months_names, climatic_means('V8_42.csv',2),linestyle = 'solid', marker = 'o', color = 'lightgreen', label='El Poal')
plt.plot(months_names, climatic_means('XI_42.csv',2), linestyle = 'solid', marker = 'o',color = 'limegreen', label='Mollerussa')
plt.plot(months_names, climatic_means('WC_42.csv',2),linestyle = 'solid', marker = 'o', color = 'seagreen', label='Golmés')
plt.plot(months_names, climatic_means('C6_42.csv',2),linestyle = 'solid', marker = 'o', color = 'darkgreen', label='Castellnou de Seana')


plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
plt.tight_layout()
#plt.savefig('Comparativa TNm.png', format='png', dpi=800)


#%% TMm DATA
gen = np.array([])
gen10 = monthly_mean('XI_32.csv',2010)[0]
gen11 = monthly_mean('XI_32.csv',2011)[0]
gen12 = monthly_mean('XI_32.csv',2012)[0]
gen13 = monthly_mean('XI_32.csv',2013)[0]
gen14 = monthly_mean('XI_32.csv',2014)[0]
gen15 = monthly_mean('XI_32.csv',2015)[0]
gen16 = monthly_mean('XI_32.csv',2016)[0]
gen17 = monthly_mean('XI_32.csv',2017)[0]
gen18 = monthly_mean('XI_32.csv',2018)[0]
gen19 = monthly_mean('XI_32.csv',2019)[0]

gen = np.append(gen, (gen10,gen11,gen12,gen13,gen14,gen15,gen16,gen17,gen18,gen19))
genmax = np.max(gen)
genmin = np.min(gen)
gen25 = np.percentile(gen,25)
gen50 = np.percentile(gen,50)
gen75 = np.percentile(gen,75)

feb = np.array([])
feb10 = monthly_mean('XI_32.csv',2010)[1]
feb11 = monthly_mean('XI_32.csv',2011)[1]
feb12 = monthly_mean('XI_32.csv',2012)[1]
feb13 = monthly_mean('XI_32.csv',2013)[1]
feb14 = monthly_mean('XI_32.csv',2014)[1]
feb15 = monthly_mean('XI_32.csv',2015)[1]
feb16 = monthly_mean('XI_32.csv',2016)[1]
feb17 = monthly_mean('XI_32.csv',2017)[1]
feb18 = monthly_mean('XI_32.csv',2018)[1]
feb19 = monthly_mean('XI_32.csv',2019)[1]

feb = np.append(feb, (feb10,feb11,feb12,feb13,feb14,feb15,feb16,feb17,feb18,feb19))
febmax = np.max(feb)
febmin = np.min(feb)
feb25 = np.percentile(feb,25)
feb50 = np.percentile(feb,50)
feb75 = np.percentile(feb,75)

mar = np.array([])
mar10 = monthly_mean('XI_32.csv',2010)[2]
mar11 = monthly_mean('XI_32.csv',2011)[2]
mar12 = monthly_mean('XI_32.csv',2012)[2]
mar13 = monthly_mean('XI_32.csv',2013)[2]
mar14 = monthly_mean('XI_32.csv',2014)[2]
mar15 = monthly_mean('XI_32.csv',2015)[2]
mar16 = monthly_mean('XI_32.csv',2016)[2]
mar17 = monthly_mean('XI_32.csv',2017)[2]
mar18 = monthly_mean('XI_32.csv',2018)[2]
mar19 = monthly_mean('XI_32.csv',2019)[2]

mar = np.append(mar, (mar10,mar11,mar12,mar13,mar14,mar15,mar16,mar17,mar18,mar19))
marmax = np.max(mar)
marmin = np.min(mar)
mar25 = np.percentile(mar,25)
mar50 = np.percentile(mar,50)
mar75 = np.percentile(mar,75)

apr = np.array([])
apr10 = monthly_mean('XI_32.csv',2010)[3]
apr11 = monthly_mean('XI_32.csv',2011)[3]
apr12 = monthly_mean('XI_32.csv',2012)[3]
apr13 = monthly_mean('XI_32.csv',2013)[3]
apr14 = monthly_mean('XI_32.csv',2014)[3]
apr15 = monthly_mean('XI_32.csv',2015)[3]
apr16 = monthly_mean('XI_32.csv',2016)[3]
apr17 = monthly_mean('XI_32.csv',2017)[3]
apr18 = monthly_mean('XI_32.csv',2018)[3]
apr19 = monthly_mean('XI_32.csv',2019)[3]

apr = np.append(apr, (apr10,apr11,apr12,apr13,apr14,apr15,apr16,apr17,apr18,apr19))
aprmax = np.max(apr)
aprmin = np.min(apr)
apr25 = np.percentile(apr,25)
apr50 = np.percentile(apr,50)
apr75 = np.percentile(apr,75)

may = np.array([])
may10 = monthly_mean('XI_32.csv',2010)[4]
may11 = monthly_mean('XI_32.csv',2011)[4]
may12 = monthly_mean('XI_32.csv',2012)[4]
may13 = monthly_mean('XI_32.csv',2013)[4]
may14 = monthly_mean('XI_32.csv',2014)[4]
may15 = monthly_mean('XI_32.csv',2015)[4]
may16 = monthly_mean('XI_32.csv',2016)[4]
may17 = monthly_mean('XI_32.csv',2017)[4]
may18 = monthly_mean('XI_32.csv',2018)[4]
may19 = monthly_mean('XI_32.csv',2019)[4]

may = np.append(may, (may10,may11,may12,may13,may14,may15,may16,may17,may18,may19))
maymax = np.max(may)
maymin = np.min(may)
may25 = np.percentile(may,25)
may50 = np.percentile(may,50)
may75 = np.percentile(may,75)

jun = np.array([])
jun10 = monthly_mean('XI_32.csv',2010)[5]
jun11 = monthly_mean('XI_32.csv',2011)[5]
jun12 = monthly_mean('XI_32.csv',2012)[5]
jun13 = monthly_mean('XI_32.csv',2013)[5]
jun14 = monthly_mean('XI_32.csv',2014)[5]
jun15 = monthly_mean('XI_32.csv',2015)[5]
jun16 = monthly_mean('XI_32.csv',2016)[5]
jun17 = monthly_mean('XI_32.csv',2017)[5]
jun18 = monthly_mean('XI_32.csv',2018)[5]
jun19 = monthly_mean('XI_32.csv',2019)[5]

jun = np.append(jun, (jun10,jun11,jun12,jun13,jun14,jun15,jun16,jun17,jun18,jun19))
junmax = np.max(jun)
junmin = np.min(jun)
jun25 = np.percentile(jun,25)
jun50 = np.percentile(jun,50)
jun75 = np.percentile(jun,75)

jul = np.array([])
jul10 = monthly_mean('XI_32.csv',2010)[6]
jul11 = monthly_mean('XI_32.csv',2011)[6]
jul12 = monthly_mean('XI_32.csv',2012)[6]
jul13 = monthly_mean('XI_32.csv',2013)[6]
jul14 = monthly_mean('XI_32.csv',2014)[6]
jul15 = monthly_mean('XI_32.csv',2015)[6]
jul16 = monthly_mean('XI_32.csv',2016)[6]
jul17 = monthly_mean('XI_32.csv',2017)[6]
jul18 = monthly_mean('XI_32.csv',2018)[6]
jul19 = monthly_mean('XI_32.csv',2019)[6]

jul = np.append(jul, (jul10,jul11,jul12,jul13,jul14,jul15,jul16,jul17,jul18,jul19))
julmax = np.max(jul)
julmin = np.min(jul)
jul25 = np.percentile(jul,25)
jul50 = np.percentile(jul,50)
jul75 = np.percentile(jul,75)

aug = np.array([])
aug10 = monthly_mean('XI_32.csv',2010)[7]
aug11 = monthly_mean('XI_32.csv',2011)[7]
aug12 = monthly_mean('XI_32.csv',2012)[7]
aug13 = monthly_mean('XI_32.csv',2013)[7]
aug14 = monthly_mean('XI_32.csv',2014)[7]
aug15 = monthly_mean('XI_32.csv',2015)[7]
aug16 = monthly_mean('XI_32.csv',2016)[7]
aug17 = monthly_mean('XI_32.csv',2017)[7]
aug18 = monthly_mean('XI_32.csv',2018)[7]
aug19 = monthly_mean('XI_32.csv',2019)[7]

aug = np.append(aug, (aug10,aug11,aug12,aug13,aug14,aug15,aug16,aug17,aug18,aug19))
augmax = np.max(aug)
augmin = np.min(aug)
aug25 = np.percentile(aug,25)
aug50 = np.percentile(aug,50)
aug75 = np.percentile(aug,75)

sept = np.array([])
sept10 = monthly_mean('XI_32.csv',2010)[8]
sept11 = monthly_mean('XI_32.csv',2011)[8]
sept12 = monthly_mean('XI_32.csv',2012)[8]
sept13 = monthly_mean('XI_32.csv',2013)[8]
sept14 = monthly_mean('XI_32.csv',2014)[8]
sept15 = monthly_mean('XI_32.csv',2015)[8]
sept16 = monthly_mean('XI_32.csv',2016)[8]
sept17 = monthly_mean('XI_32.csv',2017)[8]
sept18 = monthly_mean('XI_32.csv',2018)[8]
sept19 = monthly_mean('XI_32.csv',2019)[8]

sept = np.append(sept, (sept10,sept11,sept12,sept13,sept14,sept15,sept16,sept17,sept18,sept19))
septmax = np.max(sept)
septmin = np.min(sept)
sept25 = np.percentile(sept,25)
sept50 = np.percentile(sept,50)
sept75 = np.percentile(sept,75)

octo = np.array([])
octo10 = monthly_mean('XI_32.csv',2010)[9]
octo11 = monthly_mean('XI_32.csv',2011)[9]
octo12 = monthly_mean('XI_32.csv',2012)[9]
octo13 = monthly_mean('XI_32.csv',2013)[9]
octo14 = monthly_mean('XI_32.csv',2014)[9]
octo15 = monthly_mean('XI_32.csv',2015)[9]
octo16 = monthly_mean('XI_32.csv',2016)[9]
octo17 = monthly_mean('XI_32.csv',2017)[9]
octo18 = monthly_mean('XI_32.csv',2018)[9]
octo19 = monthly_mean('XI_32.csv',2019)[9]

octo = np.append(octo, (octo10,octo11,octo12,octo13,octo14,octo15,octo16,octo17,octo18,octo19))
octomax = np.max(octo)
octomin = np.min(octo)
octo25 = np.percentile(octo,25)
octo50 = np.percentile(octo,50)
octo75 = np.percentile(octo,75)

nov = np.array([])
nov10 = monthly_mean('XI_32.csv',2010)[10]
nov11 = monthly_mean('XI_32.csv',2011)[10]
nov12 = monthly_mean('XI_32.csv',2012)[10]
nov13 = monthly_mean('XI_32.csv',2013)[10]
nov14 = monthly_mean('XI_32.csv',2014)[10]
nov15 = monthly_mean('XI_32.csv',2015)[10]
nov16 = monthly_mean('XI_32.csv',2016)[10]
nov17 = monthly_mean('XI_32.csv',2017)[10]
nov18 = monthly_mean('XI_32.csv',2018)[10]
nov19 = monthly_mean('XI_32.csv',2019)[10]

nov = np.append(nov,(nov10,nov11,nov12,nov13,nov14,nov15,nov16,nov17,nov18,nov19))
novmax = np.max(nov)
novmin = np.min(nov)
nov25 = np.percentile(nov,25)
nov50 = np.percentile(nov,50)
nov75 = np.percentile(nov,75)

dec = np.array([])
dec10 = monthly_mean('XI_32.csv',2010)[11]
dec11 = monthly_mean('XI_32.csv',2011)[11]
dec12 = monthly_mean('XI_32.csv',2012)[11]
dec13 = monthly_mean('XI_32.csv',2013)[11]
dec14 = monthly_mean('XI_32.csv',2014)[11]
dec15 = monthly_mean('XI_32.csv',2015)[11]
dec16 = monthly_mean('XI_32.csv',2016)[11]
dec17 = monthly_mean('XI_32.csv',2017)[11]
dec18 = monthly_mean('XI_32.csv',2018)[11]
dec19 = monthly_mean('XI_32.csv',2019)[11]

dec = np.append(dec, (dec10,dec11,dec12,dec13,dec14,dec15,dec16,dec17,dec18,dec19))
decmax = np.max(dec)
decmin = np.min(dec)
dec25 = np.percentile(dec,25)
dec50 = np.percentile(dec,50)
dec75 = np.percentile(dec,75)

dadesmax = np.array([])
dadesmin = np.array([])
dadesp25 = np.array([])
dadesp50 = np.array([])
dadesp75 = np.array([])
dades = np.array([])

dades = np.append(dades, (gen,feb,mar,apr,may,jun,jul,aug,sept,octo,nov,dec))
dadesmax = np.append(dadesmax,(genmax,febmax,marmax,aprmax,maymax,junmax,julmax,augmax,septmax,octomax,novmax,decmax))
dadesmin = np.append(dadesmin,(genmin,febmin,marmin,aprmin,maymin,junmin,julmin,augmin,septmin,octomin,novmin,decmin))
dadesp25 = np.append(dadesp25, (gen25,feb25,mar25,apr25,may25,jun25,jul25,aug25,sept25,octo25,nov25,dec25))
dadesp50 = np.append(dadesp50, (gen50,feb50,mar50,apr50,may50,jun50,jul50,aug50,sept50,octo50,nov50,dec50))
dadesp75 = np.append(dadesp75, (gen75,feb75,mar75,apr75,may75,jun75,jul75,aug75,sept75,octo75,nov75,dec75))

#%% TEMPERATURE GRAPH WITH SHADOW PERCENTILES
plt.figure('TMm')
plt.grid(True)
plt.title('TMm Mollerussa')
plt.plot(months_names, dadesmax, linestyle = 'dashed', color = 'red', label='Max')  
plt.plot(months_names, dadesmin,linestyle = 'dashed', color = 'blue', label='Min') 
plt.plot(months_names, dadesp25, linestyle = 'solid', color = 'steelblue', label = 'P25', linewidth = 0.4)
plt.plot(months_names, dadesp50, linestyle = 'solid', color = 'black', label = 'P50', linewidth = 1.8)
plt.plot(months_names, dadesp75, linestyle = 'solid', color = 'salmon', label = 'P75', linewidth = 0.4)
plt.fill_between(months_names, dadesp25, dadesp75, color = 'gainsboro')  
plt.plot(months_names, monthly_mean('XI_32.csv',2021),linestyle = 'solid', marker = 'o', color = 'black', label='2021', linewidth = 0.85)

plt.legend(loc = 1)
plt.ylabel('Temperature (ºC)')
plt.tight_layout()
#plt.savefig('TMm Mollerussa.png', format='png', dpi=2000)


#%% STATISTICS TEST
from scipy.stats import skew, kurtosis
from scipy.stats import normaltest
from scipy.stats import ttest_ind
mean1 = monthly_mean('XI_32.csv',2021)
mean2 = dades
print(ttest_ind(mean1,mean2))
print(normaltest(mean1))
print(skew(mean1))
print(kurtosis(mean1))


