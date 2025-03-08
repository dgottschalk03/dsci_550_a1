import os
import random
import shutil
import glob
import subprocess
import datetime
import argparse
import json
import sys

def main(input_dir, subset_dir, out_dir, num_files, fields):

    # Check if fields is empty
    if fields == "[]":
        sys.exit("Please Select at least one field to keep.")

    # Get all JSON files
    json_files = glob.glob(os.path.join(input_dir, "*.json"))

    # Randomly select a subset
    selected_files = random.sample(json_files, min(num_files, len(json_files)))

    # Ensure subset directory exists and is empty
    if os.path.exists(subset_dir):
        shutil.rmtree(subset_dir)  # Clear existing symlinks
    os.makedirs(subset_dir)


    # Copy files and move to temp folder
    for file in selected_files:
        dest_path = os.path.join(subset_dir, os.path.basename(file))
        shutil.copy(file, dest_path)
        
        # open copy and load data
        with open(dest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # filter data and save back to copy
        filtered_data = {key: data[key] for key in fields if key in data}
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=4)

    # Remove unwanted fields from jsons #
    
    print("\n" + "-"*50 , f"\nCreated {len(selected_files)} json copies in {subset_dir}", "Now running './clones/**/jaccard_similarity.py'", sep = "\n")

    # Run jaccard_similarity.py on the temp dir
    command = [
        "python", "./clones/tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py",
        "--inputDir", subset_dir, 
        "--outCSV", out_dir
    ]
    subprocess.run(command, check=True)

    print("Finished running jaccard_similarity.py")

    # Cleanup
    shutil.rmtree(subset_dir)
    print(f"Cleaned up {subset_dir}", f"clustering csv can be found in: '{out_dir}'", sep = "\n", end = "\n" + "-"*50)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Select a random subset of JSON files and run jaccard_similarity.py on them.")

    # Define default values
    parser.add_argument("--input_dir", type=str, default="./data/tika_similarity/json", help="Directory containing JSON files (default: ./data/tika_similarity/json)")
    parser.add_argument("--subset_dir", type=str, default="./data/tika_similarity/temp", help="Temporary directory for symlinks (default: ./data/tika_similarity/temp)")
    parser.add_argument("--num_files", type=int, default=100, help="Number of JSON files to select (default: 100)")
    parser.add_argument("--out_csv", type=str, default="./clustering/jaccardSimilarity/jaccard.csv", help="Filepath for output (default: ./clustering/jaccardSimilarity/jaccard.csv)")
    parser.add_argument("--fields", type=json.loads, default=[], help="JSON list of fields to keep (e.g., '[\"name\", \"age\"]')")

    args = parser.parse_args()
    main(args.input_dir, args.subset_dir, args.out_csv, args.num_files, args.fields)


# (dsci550-py384) mattmann@MT-310349 data % python ./tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py --inputDir ./data/tika_similarity/temp/ --outCSV jaccard.csv
#  Accepting all MIME Types..... 
#  (dsci550-py384) mattmann@MT-310349 data % ls 
#  jaccard.csv	splits