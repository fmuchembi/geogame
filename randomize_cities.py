import random
import json
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk


def load_cities(geojson_path):
    features = []
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    features = geojson_data.get('features', [])
    
    return features


def current_random_city(geojson_path):
    cities = load_cities(geojson_path)

    if cities != None or cities != {}:
        random_city = random.choice(cities)  
        # Store current city data
        current_city_data = {
            'name': random_city['properties']['name'],
            'country': random_city['properties']['country'],
            'photo_url':  random_city['properties']['photo_url']
        }
        return(current_city_data)




def display_city_image(frame, random_city, image_size=(300, 300)):
    if random_city != None:
     
        photo_url = random_city['photo_url']
        name = random_city['name']
        country = random_city['country']
        print(f"current city is {name} in {country}")

        image = Image.open(photo_url)
        image = image.resize(image_size) 
        photo = ImageTk.PhotoImage(image)

        image_label = ttk.Label(frame, image=photo)
        image_label.image = photo  
        image_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")





























