import pandas as pd
from Calculator_sun_elevation_angel import df_data
from Module_grid_data import df_siste_aar
import math
import matplotlib.pyplot as plt
import locale


# Setting the time languale to Norway
locale.setlocale(locale.LC_TIME, 'no_NB') 


df_last = pd.merge(df_data,df_siste_aar)


Areal_panel = 11221 # Area with only sun configuration
#Areal_panel = 8475 # Area with sun and wind configuration

r = 0.209 # Efficensy of the solar ppanal
pr = 0.75 # The capasitefactor for on houer.

#vind_turbinder = 15 # Number of windturbin with sun and wind configuration
vind_turbinder = 45 # Number of windturbin with only wind configuration

# importing the wind turbin data.
df_wind = pd.read_excel(r'Vind_data.xlsx', engine='openpyxl')
df_wind = df_wind.rename(columns={'Vind hastigehet (m/s)': 'wind_speed' , 'Effekt i (kw)': 'Vind produkjson'})

# Find corulation with windspeed and power production
df = pd.merge(df_data, df_wind, on = 'wind_speed')


#Finding solar production from formula.
df['Sol produksjon'] =  df.apply(lambda row: Areal_panel*(r + 0.0035*(25-row['air_temperature']))*(990*math.sin(row['sea_rad']))*(1-(0.75*row['cloud_area_fraction']/100)**3.4)*pr/1000, axis=1)

df = df.drop(columns=['air_temperature', 'wind_speed', 'cloud_area_fraction','sea_deg', 'sea_rad'])


# Multiply power with nuber of turbins.
df['Vind produkjson'] = df['Vind produkjson']*vind_turbinder
df = df.drop(columns=['Vind produkjson'])
#df = df.drop(columns=['Sol produksjon'])

df.sort_values(by='time', inplace = True)

# cobin grid data with power production
df_pro = pd.merge(df_siste_aar, df , on='time')

# find total production

df_sum = pd.DataFrame()
df_sum['time'] = df_pro['time']
#df_sum['Total kapasitet'] = df_pro['Sol produksjon'] + df_pro['Vind produkjson'] + df_pro['Kapasitet sjøkabel']
df_sum['Total kapasitet'] = df_pro['Sol produksjon'] + df_pro['Kapasitet sjøkabel']
#df_sum['Total kapasitet'] =  df_pro['Vind produkjson'] + df_pro['Kapasitet sjøkabel']

# finding the mean valu of production
gjennom = df_sum['Total kapasitet'].sum()/len(df_sum.index)


# Makeing an illustation 
ax =df_pro.plot(x='time', ylabel="kWh", xlabel="Klokkeslett" , color= {"Sol produksjon": "green","Kapasitet sjøkabel": "#1f77b4"})
ax.legend(loc=5)
#ax =df_sum.plot(x='time', ylabel="kWh", xlabel="Klokkeslett", legend= 'center left')
ax.axhline(gjennom, color="red", linestyle="--")

plt.savefig('Produkjsons_data_sol.png')
#plt.savefig('Total_tilgjenegelig_data_sol.png')