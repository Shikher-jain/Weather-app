import os
import urllib.request

icons = [
    '01d.png', '02d.png', '03d.png', '04d.png', '09d.png', '10d.png',
    '11d.png', '13n.png', '50d.png', '01n.png', '02n.png', '03n.png',
    '04n.png', '09n.png', '10n.png', '11n.png', '50n.png'
]

base_url = 'https://openweathermap.org/img/w/'

# Define the directory for saving icons
img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(img_dir, exist_ok=True)

# Download icons if they don't exist
for icon in icons:
    file_path = os.path.join(img_dir, icon)
    if not os.path.exists(file_path):
        print(f"Downloading {icon}...")
        urllib.request.urlretrieve(base_url + icon, file_path)
    else:
        print(f"{icon} already exists.")
