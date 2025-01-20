import tkinter as tk
from tkinter import ttk

class initialize_geoGameview(tk.Tk):
        def __init__(self, start_size):
            super().__init__()
            self.title('Geogame')
            self.geometry(f'{start_size[0]}x{start_size[1]}')

            self.frame = ttk.Frame(self)
            self.frame.pack(expand = True, fill = 'both')

            SizeNotifier(
                self, 
                {
                    600: self.create_medium_layout, 
                    300: self.create_small_layout,
                    1200: self.create_large_layout
                })

            self.mainloop()

        def create_small_layout(self):
            self.frame.pack_forget()
            self.frame = ttk.Frame(self)
            ttk.Label(self.frame, text = 'Image', background = 'grey').pack(expand = True, fill = 'both', padx = 10, pady = 5)
            ttk.Label(self.frame, text = 'Map', background = 'white').pack(expand = True, fill = 'both', padx = 10, pady = 5)
            self.frame.pack(expand = True, fill = 'both')

        def create_medium_layout(self):
            self.frame.pack_forget()
            self.frame = ttk.Frame(self)
            
        
            self.frame.columnconfigure(0, weight = 3)  
            self.frame.columnconfigure(1, weight = 7)  
            self.frame.rowconfigure(0, weight = 1)
            
            self.frame.pack(expand = True, fill = 'both')

            ttk.Label(self.frame, text = 'Image', background = 'gray').grid(column = 0, row = 0, sticky = 'nsew', padx = 10, pady = 10)
            ttk.Label(self.frame, text = 'Map', background = 'white').grid(column = 1, row = 0, sticky = 'nsew', padx = 10, pady = 10)

        def create_large_layout(self):
            self.frame.pack_forget()
            
            self.frame = ttk.Frame(self)
            self.frame.columnconfigure(0, weight = 3)  
            self.frame.columnconfigure(1, weight = 7)  
            self.frame.rowconfigure(0, weight = 1)
            
            self.frame.pack(expand = True, fill = 'both')

            ttk.Label(self.frame, text = 'Image', background = 'gray').grid(column = 0, row = 0, sticky = 'nsew', padx = 10, pady = 10)
            ttk.Label(self.frame, text = 'Map', background = 'white').grid(column = 1, row = 0, sticky = 'nsew', padx = 10, pady = 10)

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



app = initialize_geoGameview((800,600))









