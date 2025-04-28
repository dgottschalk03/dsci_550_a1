import pandas as pd
from datetime import date
import ast
import json
import os
import base64


# Point to image
def direct_image_pointer(image_pointer, img_directory):
    return os.path.join(img_directory, image_pointer)

# Encode image date for hover info
def encode_image(image_pointer):
    with open(image_pointer, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
    return 'data:image/png;base64,{}'.format(encoded)

# Date parsing helper
def parse_date(s): 
    return date(*map(int, s.split('-'))) 

# Load Data
def load_all_data(img_directory):
    hp_df = pd.read_csv("../data/processed/haunted_places_features_added_v2.tab", sep="\t")
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: ast.literal_eval(x)) 
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: [parse_date(y) for y in x] if isinstance(x, list) else x)
    
    # Encode hpimg data
    # hp_df['Image_Pointer'] = hp_df['Image_Pointer'].apply(lambda x: direct_image_pointer(x, img_directory))
    # hp_df['Image_Pointer'] = hp_df['Image_Pointer'].apply(lambda x: encode_image(x))

    route_df = pd.read_csv("../data/joined_datasets/american_routes.tsv", sep="\t")
    route_df["Flight_Path"] = route_df["Flight_Path"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    airport_df = pd.read_csv("../data/joined_datasets/american_airports.tsv", sep="\t")
    airport_df["Airport_Radius"] = airport_df["Airport_Radius"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    with open("../data/processed/flight_proximity_data.json", "r") as f:
        flight_intersections = json.load(f)

    with open("../data/processed/airport_proximity_data.json", "r") as f:
        airport_intersections = json.load(f)

    return (
        hp_df,
        route_df,
        airport_df,
        flight_intersections,
        airport_intersections
    )