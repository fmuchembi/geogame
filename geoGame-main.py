import tkinter as tk
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
from load_world_countries import add_countries_polygons
from randomize_cities import current_random_city, display_city_image



world_countries = r"C:\Users\Faith\Desktop\msc_geoinformatics\Introduction_to_software_programming\geogame\data\world_countries.geojson"
selected_cities  = r"C:\Users\Faith\Desktop\msc_geoinformatics\Introduction_to_software_programming\geogame\data\cities.geojson"

class Initialize_GeoGameview(tk.Tk):
    def __init__(self, start_size):
        super().__init__()
        self.title('Geogame')
        self.geometry(f'{start_size[0]}x{start_size[1]}')

        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill='both')

        SizeNotifier(
            self,
            {
                600: self.create_medium_layout,
                #300: self.create_small_layout,
                1200: self.create_large_layout
            })

        self.mainloop()

    '''def create_small_layout(self):
        self.frame.pack_forget()
        self.frame = ttk.Frame(self)

        image_path = "Images\Capetown.jpg"  
        image = Image.open(image_path)
        image = image.resize((500, 300))  
        photo = ImageTk.PhotoImage(image)

        
        image_label = ttk.Label(self.frame, image=photo)
        image_label.image = photo 
        image_label.pack(expand=True, fill='both', padx=10, pady=5)

       
        map_widget = tkintermapview.TkinterMapView(self.frame, width=800, height=600)
        map_widget.pack(expand=True, fill='both', padx=10, pady=5)
        map_widget.set_position(20, 0)  
        map_widget.set_zoom(2)


    
        add_countries_polygons(map_widget, world_countries)
        self.frame.pack(expand=True, fill='both')'''

    def create_medium_layout(self):
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
            text="Photo Frame Heading", 
            style='Title.TLabel',
            wraplength=400
        )
        heading_label.grid(row=0, pady=(0, 20), sticky="nw")

        random_city = current_random_city(selected_cities)
        image_frame = ttk.Frame(left_frame, padding=2)
        image_frame.grid(row=1, sticky="nsew", pady=(0, 20))
        display_city_image(image_frame, random_city)
        
        paragraph_label = ttk.Label(
            left_frame,
            text="photo.",
            style='Description.TLabel',
            wraplength=400,
            justify="left"
        )
        paragraph_label.grid(row=2, pady=(0, 20), sticky="nw")
        
        button = tk.Button(
            left_frame, 
            text="Click Me!",
            font=('Helvetica', 12),
            bg='#2196F3',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        button.grid(row=3, pady=(0, 20), sticky="nw")
        
        map_widget = tkintermapview.TkinterMapView(
            self.frame, 
            width=800, 
            height=600, 
            corner_radius=0
            )
        map_widget.grid(row=0, column=1, sticky="nsew", padx=(20, 0))  
        map_widget.set_position(20, 0)  
        map_widget.set_zoom(2)

        add_countries_polygons(map_widget, world_countries)


    def create_large_layout(self):
        self.frame.pack_forget()

        self.frame = ttk.Frame(self)
        self.frame.columnconfigure(0, weight=3)
        self.frame.columnconfigure(1, weight=7)
        self.frame.rowconfigure(0, weight=1)

        self.frame.pack(expand=True, fill='both')
        image_path = "Images\Capetown.jpg"  
        image = Image.open(image_path)
        image = image.resize((500, 300)) 
        photo = ImageTk.PhotoImage(image)

        image_label = ttk.Label(self.frame, image=photo)
        image_label.image = photo 
        image_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")  

       
        map_widget = tkintermapview.TkinterMapView(self.frame, width=800, height=600)
        map_widget.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")  
        map_widget.set_position(20, 0)  
        map_widget.set_zoom(2)

        add_countries_polygons(map_widget, world_countries)
        self.frame.pack(expand=True, fill='both')


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


app = Initialize_GeoGameview((800, 600))
