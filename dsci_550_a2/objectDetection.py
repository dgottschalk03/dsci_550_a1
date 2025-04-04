import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

INPUT_FILE = '../data/processed/haunted_places_features_added_v2.tab'
OUTPUT_FILE = '../data/processed/haunted_places_features_added_v3.tab'
IMAGE_FOLDER = '../data/generated_images'

df = pd.read_csv(INPUT_FILE, sep='\t')

available_filenames = set(os.listdir(IMAGE_FOLDER))

model = InceptionV3(weights='imagenet')
print("InceptionV3 model loaded.")

def detect_objects_local(image_path):
    try:
        img = image.load_img(image_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        labels = decode_predictions(preds, top=5)[0]
        objects = [f"{label[1]}: {label[2]*100:.2f}%" for label in labels]
        return ', '.join(objects)
    except Exception as e:
        return str(e)

detected_objects = []

for idx, row in tqdm(df.iterrows(), total=len(df)):
    try:
        haunted_id = int(row['Haunted_Places_Id'])
    except:
        detected_objects.append('Invalid ID')
        continue

    if 0 <= haunted_id <= 7999:
        image_name = f'hpimg_{haunted_id}.png'
    elif 8000 <= haunted_id <= 9999:
        image_name = f'haunted_{haunted_id}.png'
    else:
        detected_objects.append('No image available')
        continue

    if image_name not in available_filenames:
        detected_objects.append('Image not found')
        continue

    full_image_path = os.path.join(IMAGE_FOLDER, image_name)
    objects = detect_objects_local(full_image_path)
    detected_objects.append(objects)

df['detected_objects'] = detected_objects
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, sep='\t', index=False)

print(f"Done! Detected objects saved to {OUTPUT_FILE}")
