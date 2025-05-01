import csv
import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# === SETTINGS ===
csv_path = '/Users/kater/output_folder/color_clustering.csv'  # <<-- Change this
images_folder = '/Users/kater/HauntedImages_8000'  # <<-- Change this

# === Load the color clustering CSV ===
image_clusters = {}

with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        image_clusters[row['Image']] = int(row['Cluster'])

# === Group images by cluster ===
clusters = {}
for img, cluster in image_clusters.items():
    clusters.setdefault(cluster, []).append(img)

# === Pick a random image ===
random_image = random.choice(list(image_clusters.keys()))
random_cluster = image_clusters[random_image]

print(f"Random Image: {random_image} (Cluster {random_cluster})\n")

# === Find similar images (same cluster) ===
similar_images = [img for img in clusters[random_cluster] if img != random_image]

# === Show top 5 similar images ===
print("Top 5 Similar Images:")
for i, sim_img in enumerate(similar_images[:5]):
    print(f"{i+1}. {sim_img}")

# === Plot the random image + similar images ===
fig, axes = plt.subplots(1, 6, figsize=(20, 5))

# Show the random image first
img = mpimg.imread(os.path.join(images_folder, random_image))
axes[0].imshow(img)
axes[0].axis('off')
axes[0].set_title('Query')

# Then show the top 5 similar images
for idx, sim_img in enumerate(similar_images[:5]):
    sim_img_path = os.path.join(images_folder, sim_img)
    sim_img_data = mpimg.imread(sim_img_path)
    axes[idx+1].imshow(sim_img_data)
    axes[idx+1].axis('off')
    axes[idx+1].set_title(f"Similar {idx+1}")

plt.tight_layout()
plt.show()
