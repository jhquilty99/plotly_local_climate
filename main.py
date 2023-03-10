import json
import requests
# Using opne-meteo for historical climate data
# ERA5: Generated using Copernicus Climate Change Service information 2022.
url = 'https://archive-api.open-meteo.com/v1/archive?latitude=38.80&longitude=-77.05&start_date=1971-01-01&end_date=2023-03-05&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,sunrise,sunset,shortwave_radiation_sum,precipitation_sum,snowfall_sum&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
response = requests.get(url)
response = json.loads(response.text)
print(response)