import json
import requests
import pandas as pd
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

def load_annual_data(lat, long, start, end):
    # Extract data
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={start}&end_date={end}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,sunrise,sunset,shortwave_radiation_sum,precipitation_sum,snowfall_sum&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    response = requests.get(url)
    # Load data
    response = json.loads(response.text)
    df = pd.DataFrame.from_records(response['daily'])
    # Transform data
    # Get time as a timestamp, month as a string, and year as an int
    df['time'] = df.apply(lambda x: pd.Timestamp(x['time']), axis = 1)
    df['month'] = df.apply(lambda x: datetime.date.strftime(x['time'], '%m-%b'), axis = 1)
    df['year'] = df.apply(lambda x: int(datetime.date.strftime(x['time'], '%Y')), axis = 1)
    # Derive new features from the data
    df['snowfall_chance'] = df.apply(lambda x: int(x['snowfall_sum'] > 0), axis = 1)
    df['sunrise'] = df.apply(lambda x: pd.Timestamp(x['sunrise']), axis = 1)
    df['sunset'] = df.apply(lambda x: pd.Timestamp(x['sunset']), axis = 1)
    df['sunlight_minutes'] = df.apply(lambda x: pd.Timedelta(x['sunset'] - x['sunrise']).seconds / 60.0, axis = 1)
    df['frost_day'] = df.apply(lambda x: int(x['temperature_2m_min'] <= 32), axis = 1)
    # Clean up data
    df.dropna(inplace = True)
    df = df.loc[df['year'] != '2023']
    yearly_agg_df = pd.DataFrame()
    precipitation_df = df.groupby('month').apply(lambda x: x['snowfall_chance'].mean())
    days_with_frost = df.groupby(by = 'year').apply(lambda x: x['frost_day'].sum())
    lin_regr = LinearRegression()
    lin_res = lin_regr.fit(np.array(df['year']).reshape(-1,1), np.array(df['temperature_2m_mean']))
    lin_fit = lin_regr.predict(np.array(df['year']).reshape(-1,1))