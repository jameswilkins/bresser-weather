import requests

# URL of the Flask app
url = 'http://127.0.0.1:30000/weatherstation/updateweatherstation.php'

# Parameters to be sent to the API
params = {
    'ID': '1111',
    'PASSWORD': '2222',
    'action': 'updateraww',
    'realtime': 1,
    'rtfreq': 5,
    'dateutc': 'now',
    'baromin': 29.84,
    'tempf': 53.6,
    'dewptf': 52.8,
    'humidity': 98,
    'windspeedmph': 2.9,
    'windgustmph': 3.3,
    'winddir': 169,
    'rainin': 0.095,
    'dailyrainin': 0.142,
    'solarradiation': 0.63,
    'UV': 0.0,
    'indoortempf': 71.7,
    'indoorhumidity': 53
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    print("Response from server:", response.json())
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("An Error Occurred:", err)
