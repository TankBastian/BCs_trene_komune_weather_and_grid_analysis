import requests
import pandas as pd

# Lengde og breddegrader for Træna komune
latitude = 66.6348
longitude = 12.0253


# Henter data fra API-en til Metrologisk institutt eller yr.no
met_api_url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
yr_api_url = f'http://api.yr.no/weatherapi/locationforecast/2.0/?lat={latitude};lon={longitude}'

# Idendifisere hvem brukern er
User_agent = {'User-Agent': 'sebasgsp@stud.ntnu.no'}


# hent data fra API-en
response = requests.get(met_api_url, headers = User_agent)


# Ser på om du heter rett data. 100: informasjon 200: sucess 300: vidersend, 400: feil code, 500 feil på server 
if response.status_code >= 100 and response.status_code < 400:
    
    # Konverterer json til en dictionary 
    data = response.json()

    #Finner listen med informasjon som trengs
    properties = data['properties']
    timeseries = properties['timeseries']
    
    # lager en datafame med den relevante infoen
    df_weather = pd.DataFrame(timeseries)

    # formartere data famen. Gjør tidsintervall til leselig tekst. og henter ut datan fra data og legger det til som koloner
    df_weather['time'] = pd.to_datetime(df_weather['time'], cache=True).dt.tz_localize(None)
    df_weather['air_temperature'] = df_weather['data'].apply(lambda x: x['instant']['details']['air_temperature'])
    df_weather['wind_speed'] = df_weather['data'].apply(lambda x: x['instant']['details']['wind_speed'])
    df_weather['wind_speed'] = df_weather['wind_speed'].round().astype(int)  
    df_weather['wind_from_direction'] = df_weather['data'].apply(lambda x: x['instant']['details']['wind_from_direction'])
    df_weather['cloud_area_fraction'] = df_weather['data'].apply(lambda x: x['instant']['details']['cloud_area_fraction'])





    # kvitter oss med ekstra data. Vi tar vekk vind reting for er urelevant, men kan bli relevant sener
    df_weather = df_weather.drop(columns=['data','wind_from_direction'])
    df_weather = df_weather.drop(df_weather.tail(30).index)

elif response.status_code >= 400 and response.status_code < 500:
    print(f"Client Error: {response.status_code}. Unable to fetch data from metno_locationforecast API.")
else :
    print(f"Sever Error: {response.status_code}. Unable to fetch data from metno_locationforecast API.")



print(df_weather)

