import os
import random
import shutil
import glob
import subprocess
import datetime
import argparse
import json
import sys

def main(input_dir, subset_dir, out_dir, num_files, fields, method):

    ## Check if method and fields are valid ##
    if method not in ['j', 'e', 'c']:
        sys.exit("'method' kwarg must be in ['j', 'e', 'c']. \n\t -j [jaccard] \n\t -e [edit-distance] \n\t -c [cosine] \n")
    # Check if fields is empty
    if fields == "[]":
        sys.exit("Please Select at least one field to keep.")
    # Check if in right directory
    if not os.getcwd().endswith('dsci_550_a1'):
        sys.exit("This script has relative paths from the project directory. Please run from project directory.")
    

    ## Select Similarity Script based on 'method' kwarg ##
    if method == 'j':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py"

    elif method == 'e':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/edit-value-similarity.py"

    elif method == 'c':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/cosine_similarity.py"
    
    ## Get all JSON files ##
    json_files = glob.glob(os.path.join(input_dir, "*.json"))

    # Sample a subset
    selected_files = random.sample(json_files, min(num_files, len(json_files)))

    # Ensure subset directory exists and is empty
    if os.path.exists(subset_dir):
        shutil.rmtree(subset_dir)  # Clear existing symlinks
    os.makedirs(subset_dir)


    ## Copy files and move to temp folder ##
    for file in selected_files:
        dest_path = os.path.join(subset_dir, os.path.basename(file))
        shutil.copy(file, dest_path)
        
        # open copy and load data
        with open(dest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # filter data and save back to copy

        # Ensure we are not clustering by haunted place id. This is an index and not a feature.
        if "Haunted_Places_Id" in fields:
            fields.remove("Haunted_Places_Id")

        filtered_data = {key: data[key] for key in fields if key in data}
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=4)

    # Remove unwanted fields from jsons #
    
    print("-"*50 , f"\nCreated {len(selected_files)} json copies in {subset_dir}", f"Now running '{similarity_script}'", sep = "\n")

    ## Run [method].py on the temp dir ##
    command = [
        "python", similarity_script,
        "--inputDir", subset_dir, 
        "--outCSV", out_dir
    ]
    subprocess.run(command, check=True)

    print(f"Finished running '{similarity_script}'", end = "\n" + "-"*50 + "\n") 

    ## Cleanup ##
    shutil.rmtree(subset_dir)
    print(f"Cleaned up {subset_dir}", f"clustering csv can be found in: '{out_dir}'", sep = "\n", end = "\n" + "-"*50)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Select a random subset of JSON files and run similarity metric on them.")

    # Define default values
    parser.add_argument("--input_dir", type=str, default="./data/tika_similarity/json", help="Directory containing JSON files (default: ./data/tika_similarity/json)")
    parser.add_argument("--subset_dir", type=str, default="./data/tika_similarity/temp", help="Temporary directory for symlinks (default: ./data/tika_similarity/temp)")
    parser.add_argument("--num_files", type=int, default=100, help="Number of JSON files to select (default: 100)")
    parser.add_argument("--out_csv", type=str, default="./clustering/jaccardSimilarity/jaccard.csv", help="Filepath for output (default: ./clustering/jaccardSimilarity/jaccard.csv)")
    parser.add_argument("--fields", type=json.loads, default=[], help="JSON list of fields to keep (e.g., '[\"name\", \"age\"]')")
    parser.add_argument("--method", type=str, default='j', help="Letter corresponding to clustering method \n\t -j [jaccard] \n\t -e [edit-distance] \n\t -c [cosine]")

    args = parser.parse_args()
    main(args.input_dir, args.subset_dir, args.out_csv, args.num_files, args.fields, args.method)



