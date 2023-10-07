import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def get_temperature():
    url = 'https://meteofor.com.ua/ru/weather-poznan-3194/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature_element = soup.select_one('.temperature-class')
        if temperature_element:
            return temperature_element.text.strip()
        else:
            print("Temperature not found. Check your selectors.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

def create_and_insert_data(temperature):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            temperature TEXT
        )
    ''')

    current_datetime = datetime.now()
    date = current_datetime.strftime('%Y-%m-%d')
    time = current_datetime.strftime('%H:%M:%S')

    cursor.execute('INSERT INTO weather_data (date, time, temperature) VALUES (?, ?, ?)', (date, time, temperature))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    temperature = get_temperature()

    if temperature is not None:
        create_and_insert_data(temperature)
        print(f"Data successfully added to the database. Temperature: {temperature}")
    else:
        print("Failed to get temperature data.")
