import pandas as pd
from datetime import datetime

# Les inn Excel-arket og lag en DataFrame
df = pd.read_excel(r'træna_ringnett_forbruk_2019.xlsx', engine='openpyxl')

last_cap = 8700 * 0.9     # MVA til MWh

# Bytt navn på kolonnene
df = df.rename(columns={'Dato time': 'time', 'Timeverdi (kWh)': 'Kapasitet sjøkabel'})

# Konverter tidspunkt-kolonnen til datetime-format
df['time'] = pd.to_datetime(df['time'])

# Finn året som skal brukes til å erstatte
this_year = datetime.now().year

# Lag en Series med starttidspunkt for året
year_start = pd.to_datetime(str(this_year) + '-01-01')


# Erstatt året i tidspunkt-kolonnen
df['time'] = year_start + (df['time'] - year_start.replace(year=this_year-1))

# Få tak i det siste årets data
df_siste_aar = df[df['time'] > year_start.replace(year=this_year-1)]

# Del på tilgjengelig på 4 og trekke fra 8000 på hver celle
df_siste_aar['Kapasitet sjøkabel'] = df_siste_aar['Kapasitet sjøkabel'] / 4
df_siste_aar['Kapasitet sjøkabel']  = df_siste_aar['Kapasitet sjøkabel'].apply(lambda x: last_cap - x - 4000)

# Skriv ut resultatet
print(df_siste_aar)
