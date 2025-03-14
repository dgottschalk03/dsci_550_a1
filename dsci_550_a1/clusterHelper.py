import os
import random
import shutil
import glob
import subprocess
import argparse
import json
import sys

def main(input_dir, subset_dir, out_dir, num_files, fields, method):
    """
        Computes distance between samples using input 'method'
        Helper function for clusterWorkflow.py
        Inputs:

            [input_idr]         | Directory with .json files to cluster. 
            [subset_dir]        | Directory where copied jsons are stored. Deleted after script terminates.
            [out_dir]           | Directory for outputs
            [num_files]         | determines sample of dataset used. Either [int] or [str]
                - [int]  | size of random sample. (sample generated using random.randint) 
                - [str]  | filepath to .txt specifying exact indicies to sample. 
            [fields]            | features to consider for clustering
                - "Haunted_Places_ID" hardcoded to not be used as a feature
                - if field not in .json file or misspelled, it is skipped and user is notified.
                    
            [method]            | Similarity metric used. (Credit: https://github.com/chrismattmann/tika-similarity)
                - (j)accard  | */jaccard_similarity.py
                - (e)dit     | */edit-value-similarity.py
                - (c)osine   | */cosine_similarity.py
 
        Outputs:
            [Output]             | Output of [method]_similarity.py
                - ./out_dir/[method].csv 
        Returns:
            [None]  
        NOTES:
            - You need etllib and tika-similarity installed in the "clones" directory for this script to work 
                - Tika_Similarity | https://github.com/chrismattmann/tika-similarity
                - Etllib          | https://github.com/chrismattmann/etllib
    eg use:
    >>> python clusterHelper.py 
    --input_dir "./data/tika_similarity/json_files" \
    --subset_dir "./data/tika_similarity/temp" \
    --num_files [33, 22] \
    --out_csv "./results/clustering_results.csv" \
    --fields '-a' \
    --method "j"  
    
    eg output: 
    
    STDOUT: Accepting all MIME Types.....
    --------------------------------------------------
    Selecting subset of files from ./data/tika_similarity/json
    Indicies selected: [33, 22]
    Selection Completed, indicies without a matching file: 
    [33]
    ----------------------------------------------------------------------------------------------------
    Created 1 json copies in ./data/tika_similarity/temp
    Now running './clones/tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py'
    Finished running './clones/tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py'
    --------------------------------------------------
    Cleaned up ./data/tika_similarity/temp
    clustering csv can be found in: './clustering/jaccard/hellp/jaccard.csv' 
    """
    ##############################################################################################################################
    ## Check if method and fields are valid ##

    if method not in ['j', 'e', 'c']:
        sys.exit("'method' kwarg must be in ['j', 'e', 'c']. \n\t -j [jaccard] \n\t -e [edit-distance] \n\t -c [cosine] \n")
    # Check if fields is empty
    if fields == "[]":
        sys.exit("Please Select at least one field to keep.")
    # Check if in right directory
    if not os.getcwd().endswith('dsci_550_a1'):
        sys.exit("This script has relative paths from the project directory. Please run from project directory.")
    
    ##############################################################################################################################
    ## Select Similarity Script based on 'method' kwarg ##

    if method == 'j':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/jaccard_similarity.py"

    elif method == 'e':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/edit-value-similarity.py"

    elif method == 'c':
        similarity_script = "./clones/tika-img-similarity/tikasimilarity/distance/cosine_similarity.py"
    
    ##############################################################################################################################
    ## Copy JSON files ##
    json_files = glob.glob(os.path.join(input_dir, "*.json"))

    ## If num_files is a json list, convert to list and pick those indicies ##
    if isinstance(num_files, list):
        print("-"*50 , f"Selecting subset of files from {input_dir}", f"Indicies selected: {num_files}", sep = "\n")

        selected_files = []
        selected_indicies = num_files
        
        # Open each json file and load data
        for f in json_files:
            with open(f, 'r') as f:
                data = json.load(f)

                # Add file to selected files if "Haunted_Places_Id" is in selected indicies
                if int(data['Haunted_Places_Id']) in selected_indicies:
                    selected_files.append(f.name)
                    selected_indicies.remove(int(data['Haunted_Places_Id']))

            # break early if we hit all indicies
            if len(selected_files) == len(selected_indicies):
                break
                
        print("Selection Completed, indicies without a matching file: ", selected_indicies, sep = "\n", end = "\n" + "-"*50)
   
    ## if num_files is not a json list, it must be an integer. So we randomly sample that many files ##
    else:
        selected_files = random.sample(json_files, min(num_files, len(json_files)))
    
##############################################################################################################################
## Copy files and move to temp folder ##

    # Ensure subset directory exists and is empty
    if os.path.exists(subset_dir):
        shutil.rmtree(subset_dir)  
    os.makedirs(subset_dir)

    # Copy selected fields from each .json
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
    
    print("-"*50 , f"Created {len(selected_files)} json copies in {subset_dir}", f"Now running '{similarity_script}'", sep = "\n")

##############################################################################################################################
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

##############################################################################################################################
## Custom type function for num_files argparse ##
# takes both int and json list #

def int_or_json(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return int(s)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Select a random subset of JSON files and run similarity metric on them.")

    # Define default values
    parser.add_argument("--input_dir", type=str, default="./data/tika_similarity/json", help="Directory containing JSON files (default: ./data/tika_similarity/json)")
    parser.add_argument("--subset_dir", type=str, default="./data/tika_similarity/temp", help="Temporary directory for symlinks (default: ./data/tika_similarity/temp)")
    parser.add_argument("--num_files", type=int_or_json, default=100, help="Number of JSON files to select (default: 100)")
    parser.add_argument("--out_csv", type=str, default="./clustering/jaccardSimilarity/jaccard.csv", help="Filepath for output (default: ./clustering/jaccardSimilarity/jaccard.csv)")
    parser.add_argument("--fields", type=json.loads, default=[], help="JSON list of fields to keep (e.g., '[\"name\", \"age\"]')")
    parser.add_argument("--method", type=str, default='j', help="Letter corresponding to clustering method \n\t -j [jaccard] \n\t -e [edit-distance] \n\t -c [cosine]")

    args = parser.parse_args()
    main(args.input_dir, args.subset_dir, args.out_csv, args.num_files, args.fields, args.method)



