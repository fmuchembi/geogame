
import tkinter as tk

def initialize_geoGameview():
    root = tk.Tk()
    root.title("GeoGame")
    root.geometry("800x600")

    
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    return root, canvas


root, canvas = initialize_geoGameview()


root.mainloop()


