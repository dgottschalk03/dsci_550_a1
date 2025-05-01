import pandas as pd
import spacy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import time
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("haunted_descriptions.csv")

location_data = []
for i, row in tqdm(df.iterrows(), total=len(df), desc="🔍 Extracting locations"):
    doc = nlp(row['text'])
    for ent in doc.ents:
        if ent.label_ == "GPE":
            location_data.append({
                "text": row['text'],
                "location": ent.text
            })
            break  

geolocator = Nominatim(user_agent="myGeoparser", timeout=10)

def geocode_with_retry(location, retries=3):
    for attempt in range(retries):
        try:
            return geolocator.geocode(location)
        except GeocoderTimedOut:
            print(f"⏳ Timeout: Retrying {location} (attempt {attempt + 1})")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error geocoding {location}: {e}")
            break
    return None

latitudes = []
longitudes = []

for entry in tqdm(location_data, desc="🌍 Geocoding"):
    geo = geocode_with_retry(entry["location"])
    if geo:
        latitudes.append(geo.latitude)
        longitudes.append(geo.longitude)
    else:
        latitudes.append(None)
        longitudes.append(None)
    time.sleep(1)

for i in range(len(location_data)):
    location_data[i]['latitude'] = latitudes[i]
    location_data[i]['longitude'] = longitudes[i]


geo_df = pd.DataFrame(location_data)
geo_df = geo_df.dropna(subset=["latitude", "longitude"])
geo_df.to_csv("parsed_haunted_locations.csv", index=False)
print("Saved parsed_haunted_locations.csv")

m = folium.Map(location=[39.5, -98.35], zoom_start=4)

for _, row in geo_df.iterrows():
    folium.CircleMarker(
        location=(row["latitude"], row["longitude"]),
        radius=5,
        popup=row["text"],
        fill=True,
        color="red",
        fill_opacity=0.7
    ).add_to(m)

m.save("haunted_map.html")
print("Map saved as haunted_map.html")

