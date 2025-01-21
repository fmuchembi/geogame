import json

def add_countries_polygons(map_widget, geojson_file):
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
        try:
            if geometry.get("type") == "Polygon":
                for coords in geometry.get("coordinates", []):
                    polygon_coords = [(coord[1], coord[0]) for coord in coords]
                    if polygon_coords: 
                        map_widget.set_polygon(polygon_coords, 
                                               outline_color="blue",
                                               fill_color="lightblue",
                                               name=country_name)
            
            elif geometry.get("type") == "MultiPolygon":
                for polygon in geometry.get("coordinates", []):
                    for coords in polygon:
                        polygon_coords = [(coord[1], coord[0]) for coord in coords]
                        
                        if polygon_coords:
                            map_widget.set_polygon(polygon_coords,
                                                   outline_color="blue",
                                                   fill_color="lightblue",
                                                   name=country_name)
        except Exception as e:
            print(f"Error processing {country_name}: {str(e)}")
            continue

