
import requests
from datetime import datetime, timedelta

API_KEY = "PUT THE KEY HERE"
CITY_NAME = "Portland,US"
def get_current_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    data = response.json()
    return data

def is_currently_raining(data):
    return 'rain' in data

def get_forecast():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    return response.json()

def will_rain_next_three_days(forecast_data):
    now = datetime.now()
    end_time = now + timedelta(days=3)
    rain_times = []

    for entry in forecast_data.get('list', []):
        forecast_time = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
        if now <= forecast_time <= end_time and 'rain' in entry:
            rain_times.append(entry['dt_txt'])

    return rain_times



# Question A
weather_now = get_current_weather()
if is_currently_raining(weather_now):
    print("A.Yes, it is currently raining in Portland, OR.")
else:
    print("A.No, it is not raining in Portland, OR right now.")

# Question B
forecast = get_forecast()
rain_schedule = will_rain_next_three_days(forecast)

if rain_schedule:
    print("B.Yes, it is forecasted to rain in Portland within the next 3 days.")
    print("Rain expected at:")
    for time in rain_schedule:
        print(f"  - {time}")
else:
    print("B.No, no rain is forecasted in Portland within the next 3 days.")
