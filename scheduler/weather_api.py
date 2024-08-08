import requests

def fetch_weather(city):
    api_key = '265960e484484c69be190222242307'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
        return None