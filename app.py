from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import requests

app = Flask(__name__)

# List of cities
cities = ['Bangalore', 'New York', 'Sydney', 'Tokyo', 'Dublin']

def fetch_weather_data():
    api_key = '3d94d653fc754e72bf868f7531136541'
    weather_data = []
    for city in cities:
        try:
            # Fetch coordinates
            response = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}')
            coords = response.json()['results'][0]['geometry']
            lat, lon = coords['lat'], coords['lng']
            
            # Fetch weather data
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true')
            weather = response.json()['current_weather']
            
            weather_data.append({
                'city': city,
                'temperature': weather['temperature']
            })
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
            weather_data.append({
                'city': city,
                'temperature': None
            })
    
    return weather_data

def plot_weather_data(weather_data):
    df = pd.DataFrame(weather_data)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='city', y='temperature', data=df, palette='viridis')
    plt.title('Current Temperature by City')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather_plot')
def weather_plot():
    weather_data = fetch_weather_data()
    img = plot_weather_data(weather_data)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
