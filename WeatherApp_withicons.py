import tkinter as tk
import requests
import os
from PIL import Image, ImageTk
from dotenv import load_dotenv

# Load API key from .env file (recommended)
load_dotenv()
weather_key = os.getenv("WEATHER_API_KEY")  # Put this in a .env file as WEATHER_API_KEY=your_key

app = tk.Tk()
app.title("Weather App")

# Constants
PATH = os.path.dirname(os.path.abspath(__file__))
HEIGHT = 500
WIDTH = 600
IMG_DIR = os.path.join(PATH, 'img')

def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description'].capitalize()
        temp = weather_json['main']['temp']
        return f'City: {city}\nConditions: {conditions}\nTemperature (°C): {temp}'
    except:
        return 'There was a problem retrieving that information'

def get_weather(city):
    if not city:
        results['text'] = "Please enter a city name."
        return

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units': 'metric'}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_json = response.json()
        results['text'] = format_response(weather_json)

        icon_name = weather_json['weather'][0]['icon']
        open_image(icon_name)

    except requests.exceptions.RequestException as e:
        results['text'] = f"Network error: {e}"
    except Exception:
        results['text'] = "Error: Could not retrieve weather information."

def open_image(icon):
    try:
        size = int(lower_frame.winfo_height() * 0.25)
        icon_path = os.path.join(IMG_DIR, icon + '.png')
        img = Image.open(icon_path).resize((size, size))
        img = ImageTk.PhotoImage(img)

        weather_icon.delete("all")
        weather_icon.create_image(0, 0, anchor='nw', image=img)
        weather_icon.image = img
    except Exception as e:
        print(f"Error loading icon: {e}")

# Main Canvas
C = tk.Canvas(app, height=HEIGHT, width=WIDTH)
background_path = os.path.join(PATH, 'landscape.png')
background_image = tk.PhotoImage(file=background_path)
background_label = tk.Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()

# Input Frame
frame = tk.Frame(app, bg='#42c2f4', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

textbox = tk.Entry(frame, font=("Helvetica", 12))
textbox.place(relwidth=0.65, relheight=1)

submit = tk.Button(frame, text='Get Weather', font=("Helvetica", 12), command=lambda: get_weather(textbox.get()))
submit.place(relx=0.7, relheight=1, relwidth=0.3)

# Output Frame
lower_frame = tk.Frame(app, bg='#42c2f4', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

bg_color = 'white'
results = tk.Label(lower_frame, anchor='nw', justify='left', bd=4, bg=bg_color, font=("Helvetica", 12))
results.place(relwidth=1, relheight=1)

weather_icon = tk.Canvas(results, bg=bg_color, bd=0, highlightthickness=0)
weather_icon.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5)

app.mainloop()
