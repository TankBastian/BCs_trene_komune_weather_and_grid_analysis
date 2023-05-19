# regner ut sol vinkle

from Get_weather_api import latitude, longitude, df_weather
import math
import datetime
import pandas as pd


# Function witch take Latitude, longitude, time and date to find solar  eleavtion angel
def getSEA(latitude, longitude, utc_offset, date):
    hour = date.hour
    minute = date.minute
    second = date.second

    # Round down to the nearest hour
    date = date.replace(minute=0, second=0, microsecond=0)

    # Check your timezone to add the offset
    hour_minute = (hour + minute / 60) - utc_offset
    day_of_year = date.timetuple().tm_yday

    g = (360 / 365.25) * (day_of_year + hour_minute / 24)

    g_radians = math.radians(g)

    declination = 0.396372 - 22.91327 * math.cos(g_radians) + 4.02543 * math.sin(g_radians) - 0.387205 * math.cos(
        2 * g_radians) + 0.051967 * math.sin(2 * g_radians) - 0.154527 * math.cos(3 * g_radians) + 0.084798 * math.sin(
        3 * g_radians)

    time_correction = 0.004297 + 0.107029 * math.cos(g_radians) - 1.837877 * math.sin(g_radians) - 0.837378 * math.cos(
        2 * g_radians) - 2.340475 * math.sin(2 * g_radians)

    SHA = (hour_minute - 12) * 15 + longitude + time_correction

    if (SHA > 180):
        SHA_corrected = SHA - 360
    elif (SHA < -180):
        SHA_corrected = SHA + 360
    else:
        SHA_corrected = SHA

    lat_radians = math.radians(latitude)
    d_radians = math.radians(declination)
    SHA_radians = math.radians(SHA_corrected)

    SZA_radians = math.acos(
        math.sin(lat_radians) * math.sin(d_radians) + math.cos(lat_radians) * math.cos(d_radians) * math.cos(
            SHA_radians))

    SZA = math.degrees(SZA_radians)

    SEA = 90 - SZA

    if math.radians(SEA) < 0:
        SEA = 0

    return math.radians(SEA), SEA


# Making a datafram with the function for finding the SEA (Solar elevation angel).
def create_dataframe(latitude, longitude, utc_offset, hours):
    now = datetime.datetime.now()
    # Round down to the nearest hour
    now = now.replace(minute=0, second=0, microsecond=0)
    time_list = [now + datetime.timedelta(hours=i) for i in range(hours)]
    sea_list = []
    sea_deg_list = []
    time_str_list = []

    for t in time_list:
        sea, sea_deg = getSEA(latitude, longitude, utc_offset, t)
        sea_list.append(sea)
        sea_deg_list.append(max(0, sea_deg))  # Sett negativ verdi til 0
        time_str_list.append(pd.to_datetime(t))

    df = pd.DataFrame({
        "time": time_str_list,
        "sea_deg": sea_deg_list,
        "sea_rad": sea_list,
    })

    return df


# Varibals for Træna kommune.
latitude = 66.6348
longitude = 12.0253
utc_offset = 2
hours = 55


# Start on a datafame
df = create_dataframe(latitude, longitude, utc_offset, hours)


# merg the weather fame to add the SEA to weather frame
df_data= pd.merge(df_weather, df, on='time')
