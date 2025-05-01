import argparse
import csv
import pickle
import numpy as np
import cv2
import os

def main():
    parser = argparse.ArgumentParser(description="Image histogram clustering")
    parser.add_argument("image_list", help="Path to text file listing image filenames")
    parser.add_argument("--opath", required=True, help="Output directory path")
    parser.add_argument("--cluster_count", type=int, default=3, help="Number of clusters for k-means")
    args = parser.parse_args()

    # Load image filenames
    with open(args.image_list, 'r') as f:
        image_files = [line.strip() for line in f if line.strip()]

    print(f"Loaded {len(image_files)} images from {args.image_list}")

    feature_matrix = []

    for img_file in image_files:
        img = cv2.imread(img_file)
        if img is None:
            print(f"Warning: Could not read image {img_file}")
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        feature_matrix.append(hist)

    feature_matrix = np.array(feature_matrix)

    print(f"Feature matrix shape: {feature_matrix.shape}")

    # K-means clustering
    term_crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    ret, labels, centers = cv2.kmeans(
        np.float32(feature_matrix),
        int(args.cluster_count),
        None,  # no initial labels
        term_crit,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    label_list = [int(l[0]) for l in labels]
    print(f"Generated {args.cluster_count} clusters.")

    # Save clustering result
    if not os.path.exists(args.opath):
        os.makedirs(args.opath)

    output_csv = os.path.join(args.opath, "color_clustering.csv")
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image', 'Cluster'])
        for img, label in zip(image_files, label_list):
            writer.writerow([img, label])

    print(f"Cluster assignments saved to {output_csv}")

    # Save pickle
    image_label = list(zip(image_files, label_list))
    output_pickle = os.path.join(args.opath, "color_clustering.p")
    with open(output_pickle, 'wb') as pfile:
        pickle.dump(image_label, pfile)

    print(f"Pickle saved to {output_pickle}")

if __name__ == "__main__":
    main()

