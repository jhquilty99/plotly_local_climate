import json
import requests
import pandas as pd
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import random
import os

def generateRowId():
  ts = int(datetime.datetime.now().timestamp())
  randid = random.randrange(0,512)
  return str(ts)+str(randid)

def reverse_geocoding(lat = 38.80, long = -77.05):
    open_meteo_api_key = os.environ['OPEN_METEO_API_KEY']
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={str(lat)}&lon={str(long)}&apiKey={str(open_meteo_api_key)}"
    resp = requests.get(url)
    df = pd.DataFrame.from_records(resp.json()['features'][0]['properties'])
    return(str(df.iloc[0]['formatted']))

def load_solar_data(lat = 38.80, long = -77.05):
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={str(lat)}&longitude={str(long)}&start_date=2020-01-02&end_date=2021-01-01&daily=sunrise,sunset&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    response = requests.get(url)
    # Load data
    response = json.loads(response.text)
    df = pd.DataFrame.from_records(response['daily'])
    df['time'] = df.apply(lambda x: pd.Timestamp(x['time']), axis = 1)
    df['sunrise'] = df.apply(lambda x: pd.Timestamp(x['sunrise']), axis = 1)
    df['sunset'] = df.apply(lambda x: pd.Timestamp(x['sunset']), axis = 1)
    df['sunlight_minutes'] = df.apply(lambda x: pd.Timedelta(x['sunset'] - x['sunrise']).seconds / 60.0, axis = 1)
    return(df)

def load_annual_data(lat = 38.80, long = -77.05, start = '1960-01-01', end = '2023-03-05'):
    # Extract data
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={str(lat)}&longitude={str(long)}&start_date={start}&end_date={end}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,shortwave_radiation_sum,precipitation_sum,snowfall_sum&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    response = requests.get(url)
    # Load data
    response = json.loads(response.text)
    df = pd.DataFrame.from_records(response['daily'])
    # Transform data
    # Get time as a timestamp, month as a string, and year as an int
    df['time'] = df.apply(lambda x: pd.Timestamp(x['time']), axis = 1)
    df['day'] = df.apply(lambda x: datetime.date.strftime(x['time'], '%e'), axis = 1)
    df['month'] = df.apply(lambda x: datetime.date.strftime(x['time'], '%m-%b'), axis = 1)
    df['year'] = df.apply(lambda x: int(datetime.date.strftime(x['time'], '%Y')), axis = 1)
    # Clean up data
    df.dropna(inplace = True)
    df = df.loc[df['year'] != int(start[0:4])]
    df = df.loc[df['year'] != int(end[0:4])]
    # Derive new features from the data
    df['snow_day'] = df.apply(lambda x: int(x['snowfall_sum'] > 0), axis = 1)
    df['frost_day'] = df.apply(lambda x: int(x['temperature_2m_min'] <= 32), axis = 1)
    monthly_agg_df = pd.DataFrame()
    # Derive new features for the monthly data
    monthly_agg_df['snow_day'] = df.groupby(by = 'month').apply(lambda x: x['snow_day'].mean())
    monthly_agg_df['frost_day'] = df.groupby(by = 'month').apply(lambda x: x['frost_day'].mean())
    yearly_agg_df = pd.DataFrame()
    # Derive new features for the yearly data
    yearly_agg_df['snow_day'] = df.groupby(by = 'year').apply(lambda x: x['snow_day'].mean())
    yearly_agg_df['frost_day'] = df.groupby(by = 'year').apply(lambda x: x['frost_day'].mean())
    yearly_agg_df['avg_mean_temp'] = df.groupby('year').apply(lambda x: x['temperature_2m_mean'].mean())
    yearly_agg_df['avg_min_temp'] = df.groupby('year').apply(lambda x: x['temperature_2m_min'].mean())
    yearly_agg_df['avg_max_temp'] = df.groupby('year').apply(lambda x: x['temperature_2m_max'].mean())
    return(df, monthly_agg_df, yearly_agg_df)


def lin_reg_fit(df, y, x = None):
    # Linear regression to fit ols trendline
    lin_regr = LinearRegression()
    if isinstance(x, str):
        lin_res = lin_regr.fit(np.array(df[x]).reshape(-1,1), np.array(df[y]))
        lin_array = lin_regr.predict(np.array(df[x]).reshape(-1,1))
    else:
        lin_res = lin_regr.fit(np.array(df.index).reshape(-1,1), np.array(df[y]))
        lin_array = lin_regr.predict(np.array(df.index).reshape(-1,1))
    return(lin_array, lin_res.coef_[0])
