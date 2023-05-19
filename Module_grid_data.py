import pandas as pd
from datetime import datetime

# Get the grid data
df = pd.read_excel(r'træna_ringnett_forbruk_2019.xlsx', engine='openpyxl')

last_cap = 8700 * 0.9     # MVA til MWh

# Changing name
df = df.rename(columns={'Dato time': 'time', 'Timeverdi (kWh)': 'Kapasitet sjøkabel'})

# Converting to the right time data
df['time'] = pd.to_datetime(df['time'])

# Find this year
this_year = datetime.now().year

# Make at time series of all date of the yer form today
year_start = pd.to_datetime(str(this_year) + '-01-01')


# replac all olde time stamps with new
df['time'] = year_start + (df['time'] - year_start.replace(year=this_year-1))

# Cut away all olde data
df_siste_aar = df[df['time'] > year_start.replace(year=this_year-1)]

# Scaling data and finding capasat on the data.
df_siste_aar['Kapasitet sjøkabel'] = df_siste_aar['Kapasitet sjøkabel'] / 4
df_siste_aar['Kapasitet sjøkabel']  = df_siste_aar['Kapasitet sjøkabel'].apply(lambda x: last_cap - x - 4000)

