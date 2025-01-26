import tkinter as tk
from tkinter import ttk
import tkintermapview
import json
from randomize_cities import current_random_city, display_city_image



world_countries = r"data\world_countries.geojson"
selected_cities  = r"data\cities.geojson"

class InitializeGeoGameview(tk.Tk):
    def __init__(self, start_size):
        super().__init__()
        self.title('Geogame')
        self.geometry(f'{start_size[0]}x{start_size[1]}')

        self.random_city = current_random_city(selected_cities)

        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill='both')

        SizeNotifier(
            self,
            {
                600: self.create_medium_layout,
                1200: self.create_large_layout
            })

        self.mainloop()


    def on_button_click(self):
        self.random_city = current_random_city(selected_cities)
        self.update_city_image()
        self.paragraph_label.config(text="")
        
        #print("Button clicked! New city generated.")

    def update_city_image(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        display_city_image(self.image_frame, self.random_city)

    def polygon_click(self, polygon):
        if self.random_city:
            if self.random_city['country'].lower() == polygon.name.lower():
                self.paragraph_label.config(text=f"Yeey! {self.random_city['name']} is indeed in {polygon.name}")
            else:
                self.paragraph_label.config(text=f"Noo fail! {self.random_city['name']} is in {self.random_city['country']}, not {polygon.name}")
    

    def add_countries_polygons(self, map_widget, geojson_file):
        try:
            with open(geojson_file, "r") as file:
                geojson_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{geojson_file}' was not found.")
            return
        except json.JSONDecodeError:
            print(f"Error: The file '{geojson_file}' is not a valid GeoJSON file.")
            return

        for feature in geojson_data.get("features", []):
            geometry = feature.get("geometry", {})
            properties = feature.get("properties", {})
            country_name = properties.get("name", "Unknown")
            iso_name = properties.get("iso_a3", "Unknown")
            try:
                if geometry.get("type") == "MultiPolygon":
                    for polygon in geometry.get("coordinates", []):
                        coords = polygon[0]  
                        centroid_lon = sum(coord[0] for coord in coords) / len(coords)
                        centroid_lat = sum(coord[1] for coord in coords) / len(coords)
                        polygon_coords = [(coord[1], coord[0]) for coord in coords]
                        if polygon_coords:
                            map_widget.set_polygon(
                                polygon_coords,
                                outline_color="gray",
                                fill_color="lightblue",
                                border_width=0.5,
                                command=self.polygon_click,
                                name=country_name
                            )
                ##polygon.bind("<Button-1>", lambda event, name=country_name: print(f"Clicked on: {name}"))
            except Exception as e:
                print(f"Error processing {iso_name}: {str(e)}")

    def create_medium_layout(self):
       self._create_layout()

    def create_large_layout(self):
        self._create_layout()

    def _create_layout(self):
        self.frame.pack_forget()
        self.frame = ttk.Frame(self)
        
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Description.TLabel', font=('Helvetica', 12))
        
        self.frame.columnconfigure(0, weight=3)
        self.frame.columnconfigure(1, weight=7)
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        left_frame = ttk.Frame(self.frame, padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        for i in range(4):
            left_frame.rowconfigure(i, weight=1)
        
        heading_label = ttk.Label(
            left_frame, 
            text="How well do you know the world!!!!!", 
            style='Title.TLabel',
            wraplength=400
        )
        heading_label.grid(row=0, pady=(0, 20), sticky="nw")
        
        self.image_frame = ttk.Frame(left_frame, padding=2)
        self.image_frame.grid(row=1, sticky="nsew", pady=(0, 20))
        display_city_image(self.image_frame, self.random_city)
        
        self.paragraph_label = ttk.Label(
            left_frame,
            text=' ',
            style='Description.TLabel',
            wraplength=400,
            justify="left"
        )
        self.paragraph_label.grid(row=2, pady=(0, 20), sticky="nw")
        
        button = tk.Button(
            left_frame, 
            text="Continue!",
            font=('Helvetica', 12),
            bg='#2196F3',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.on_button_click  
        )
        button.grid(row=3, pady=(0, 20), sticky="nw")

        country_name_label = ttk.Label(
        self.frame, 
        text="Country Name",
        style='Description.TLabel'
         )
        country_name_label.grid(row=0, column=1, sticky="nw", padx=(20, 0), pady=10)
        
        map_widget = tkintermapview.TkinterMapView(
            self.frame,
            width=800,
            height=600,
            corner_radius=0
        )

        map_widget.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        map_widget.set_position(20, 0)
        map_widget.set_zoom(1)
        
        self.add_countries_polygons(map_widget, world_countries)

class SizeNotifier:
    def __init__(self, window, size_dict):
        self.window = window
        self.size_dict = {key: value for key, value in sorted(size_dict.items())}
        self.current_min_size = None
        self.window.bind('<Configure>', self.check_size)

        self.window.update()

        min_height = self.window.winfo_height()
        min_width = list(self.size_dict)[0]
        self.window.minsize(min_width, min_height)

    def check_size(self, event):
        if event.widget == self.window:
            window_width = event.width
            checked_size = None

            for min_size in self.size_dict:
                delta = window_width - min_size
                if delta >= 0:
                    checked_size = min_size

            if checked_size != self.current_min_size:
                self.current_min_size = checked_size
                self.size_dict[self.current_min_size]()


app = InitializeGeoGameview((800, 600))
