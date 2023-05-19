import requests
import pandas as pd

# Longtitdu and Latitud for Træna kommune
latitude = 66.6348
longitude = 12.0253


# Url for api server
met_api_url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
yr_api_url = f'http://api.yr.no/weatherapi/locationforecast/2.0/?lat={latitude};lon={longitude}'

# Identify you as a user for the server
User_agent = {'User-Agent': 'User@gmail.com'}


# feach api data
response = requests.get(met_api_url, headers = User_agent)


# check if it erro cod in fecching data
if response.status_code >= 100 and response.status_code < 400:
    
    # Converting for json dictonary 
    data = response.json()

    #exstract the data from dictonary
    properties = data['properties']
    timeseries = properties['timeseries']
    
    # make a datafram form data
    df_weather = pd.DataFrame(timeseries)

    # separating data
    df_weather['time'] = pd.to_datetime(df_weather['time'], cache=True).dt.tz_localize(None)
    df_weather['air_temperature'] = df_weather['data'].apply(lambda x: x['instant']['details']['air_temperature'])
    df_weather['wind_speed'] = df_weather['data'].apply(lambda x: x['instant']['details']['wind_speed'])
    df_weather['wind_speed'] = df_weather['wind_speed'].round().astype(int)  
    df_weather['wind_from_direction'] = df_weather['data'].apply(lambda x: x['instant']['details']['wind_from_direction'])
    df_weather['cloud_area_fraction'] = df_weather['data'].apply(lambda x: x['instant']['details']['cloud_area_fraction'])





    # discarding unsude data.
    df_weather = df_weather.drop(columns=['data','wind_from_direction'])
    df_weather = df_weather.drop(df_weather.tail(30).index)

elif response.status_code >= 400 and response.status_code < 500:
    print(f"Client Error: {response.status_code}. Unable to fetch data from metno_locationforecast API.")
else :
    print(f"Sever Error: {response.status_code}. Unable to fetch data from metno_locationforecast API.")


