
# DATA PROCESSING OF THE LIASE ZONE CAMPAIGN 

This project consists of a collection of Python scripts that process data from the SMC - XEMA (Xarxa d'Estacions Meteorolgiques Automàtiques) and may be used to generate plots for a variety of climatological parameters.

All of the files are user-friendly and may be customized to fit any of the available stations.


The primary goal of this study was to examine the climate trend of the LIASE Zone during the 2021 campaign.
It also takes into account a ten-year reference period (2010-2019) in order to compare and contrast possible changes.


The data has been obtained in csv format from the XEMA website using the filtering tool it provides (divided by station code and climate constant code).


The project is broken down into several python scripts. They have to be openeded using a python accessible program like Spyder or Jupiter notebook.
All of them follow the same structure and have to be initialize making sure the data files are in the same directory as the python file.

- TEMPERATURES
This python script lets us open a pandas' data frame importing our csv data. I used pandas library because of its high performance working with csv files.
This data frame can be split into different ones using a series of functions. We can obtain temperature graphs, boxplots and shadowed graphs showing percentiles.
The last cell of the script allows us to perform a statistics test on a single csv file plus to determine parameters like the kurtosis and the skew.
The extrem values (max and min temperatures) are obtained daily and rescaled later into months.

- PRECIPITACIO 
With this script we can obtain bar graphs of the monthly accumulated precipitation
as well as the monthly maximum precipitation registered in 1 hour. For an easy comparison
we can also plot the mean line correspoding to the time series of the reference period and generate boxplots.

- VENTS 
This script lets us obtain a variety of plots involving the wind parameters.
First we can get daily graphs representing the variation of the wind direction.
We can also plot a figure with 2 subplots that show for two different stations the daily variation
of the wind speed, wind direction and the mean temperature curve.
The main goal of this script is the final section where we can generate the different wind roses
for a three-hourly period. These roses can be obtained using the daily function or the monthly mean one.

- MITJANA ESTACIONAL
Using 3 functions we can divide the values by season and obtain the plots for an individual year or the mean for the 2010-2019 time series. 
In this script I used the precipitation values expressen by the '_35.csv' format on the name of the files. 
The [i] with i=0,1,2,3,4 are as follow: 0-winter, 1-spring, 2-summer, 3-fall, 4-means.

- WEEKLYDATA 
To obtain weekly graphs this script lets us select a range of weeks.
It has been selected the weeks corresponding to July and August 2021. 
In order to plot the extrem temperatures the code is missing revision (so we can only obtain with certainty
the values for the mean temperature and the accumulated precipitation).

- 2022 
This scripts is a compilation of the temperature and precipitation ones, modified to fit the
MAY 2021 - APRIL 2022 time period. 


- aemet
The user can generate an Api Key and gain access to the official AEMET website using the first segment of the code.

The key can only be used for a week before needing to be changed by accessing a link.

The code returns a second link that has the data in json format; to convert it to csv files, we may go to any website that supports such conversions.
The script's second section creates monthly graphs and can also plot the SMC data (merge of the stations).


#### Quality control applied to each file:
Each initial data frame contains a separate column with a verification parameter (V, F, or blank); we are only interested in valid values (V).

If more than 80% of the original data is verified, the read() function returns a data frame containing only the verified values.

If necessary, this can be applied to any of the other functions. 


## Authors

- [@martabalague](https://www.github.com/martabalague)


## Documentation

- [XEMA Data](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-de-la-XEMA/nzvn-apee/data)
- [XEMA Metadata](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Metadades-variables-meteorol-giques/4fb2-n3yi/data)
- [Pandas Documentation](https://pandas.pydata.org/docs/user_guide/index.html)
- [AEMET Api Key](https://opendata.aemet.es/centrodedescargas/altaUsuario?)
- [JSON to CSV](https://www.convertcsv.com/json-to-csv.htm)


## Used By

This project is being used by Universitat de Barcelona, METEO-UB group.

## Support

For support, email mbalague@meteo.ub.edu. or mbalagma16@alumnes.ub.edu


## FAQ

#### How do I select a specific station?

Wherever there is a 'nomfitxer' or similar being used, you have to enter the station
required by the format of the string: STATIONCODE_CLIMATICCONSTANTCODE.csv

#### Why does it ask me to introduce a file name and a year?
The script has a user friendly function when initializing the different parts of the code.
If it asks for a file name you have to type down STATIONCODE_CLIMATICCONSTANTCODE.csv (only it will accept as valid this format)
and the year has to be in the [2009-2022] range.

## Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| lightgreen | ![#90E90](https://via.placeholder.com/10/90ee90?text=+) #90ee90 |
| limegreen | ![#32cd32](https://via.placeholder.com/10/32cd32?text=+) #32cd32 |
| seagreen | ![#2E8B57](https://via.placeholder.com/10/2E8B57?text=+) #2e8b57 |
| darkgreen | ![#006400](https://via.placeholder.com/10/006400?text=+) #006400 |

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| lightcoral | ![#f08080](https://via.placeholder.com/10/f08080?text=+) #f08080 |
| indianred | ![#CD5C5C](https://via.placeholder.com/10/CD5C5C?text=+) #cd5c5c |
| firebrick | ![#b22222](https://via.placeholder.com/10/b22222?text=+) #b22222 |
| maroon| ![#800000](https://via.placeholder.com/10/800000?text=+) #800000 |
