'''
Sets up json folders for clustering. To run, cd to data directory and run command "python ../dsci_550_a1/jaccardClusterWorkflow.py"
'''
# System Path #
import os
import sys 
import shutil
import subprocess
import pandas as pd
import subprocess
import time
import json

##############################################################################################################################

## Making Directories ##

## Check cwd. if not in project director, prompt user##
starting_dir = os.getcwd()

if not starting_dir.endswith("dsci_550_a1"):
    x = input("This script has relative paths from the project directory. Are you sure you want to continue? (y/n):")
    if x.strip().lower() == "y":
        pass
    else:
        sys.exit("Script exited")

## Get clustering type ##
cluster_char = ''
while cluster_char not in ['j', 'e', 'c']:
    cluster_char = input("Enter a clustering type: \n\t -j [jaccard] \n\t -e [edit-distance] \n\t -c [cosine] \n" + '-'*50 + "\n" + "Choice: ").lower()
    
if cluster_char == 'j':
    clustering_method = 'jaccard'
    circle_packing_kwarg = '2'
    
# edit distance requires circle packing kwarg of 0 
elif cluster_char == 'e':
    clustering_method = 'edit-distance'
    circle_packing_kwarg = '0'

elif cluster_char == 'c':
    clustering_method = 'cosine'
    circle_packing_kwarg = '2'

## Create clustering output directory ##
if not os.path.exists("./clustering"):
    os.makedirs("./clustering")

clustering_subdir = os.path.join("./clustering", clustering_method)

if not os.path.exists(clustering_subdir):
    os.makedirs(clustering_subdir)



## Create directories for aggregate.json, json, and conf files  in data folder ##

parent_dir = "./data/tika_similarity"
child_dirs = ["aggregate_json", "conf", "json", "temp", "clusters"]

os.makedirs(parent_dir, exist_ok = True)
for child in child_dirs:
    os.makedirs(os.path.join(parent_dir, child), exist_ok = True)


##############################################################################################################################

## User input ##
# user inputs fields to cluster by and files they wish to cluster


outfile = "./data/processed/haunted_places_features_added.tab"
columns = pd.read_csv(outfile, nrows = 0, sep = "\t").columns.tolist()

#########################################################
## Selecting subset of files  ##

num_files = '' 
while not num_files.isdigit() or not (0 < int(num_files) <= 10992):
    num_files = input("\n" + '-'*50 + "\nEnter number of haunted places to cluster: \n\nType \"-1\" to input a list of custom indicies \n" + '-'*50 + "\n" + "Choice: ").strip()

    ## If user selects -1, prompt to input list
    if num_files == '-1': 

        while True: 
            num_files = input("Enter a list of indicies corresponding to haunted places in \"haunted_places_features_added.tab\" (e.g., '[1, 2, 3]'):  \n" + '-'*50 + "\n" + "Choice: ").strip()
            # Check if list is in valid format
            try: 
                num_files_check = json.loads(num_files)
                # Break loop if list is valid and all entries are integers within 0, 10991
                if isinstance(num_files_check, list) and all ((isinstance(num, int) and 0 <= num <= 10991) for num in num_files_check):
                    break
                else:
                    print("Error: Please enter a valid list of integers within range [0, 10991].")
            except json.JSONDecodeError:
                print("Make sure your list is in proper json list format  (e.g., '[1, 2, 3]')")
        break
        
num_files = num_files

#########################################################
## Field Selection ##

## subset of fields you want to consider
fields = ''
while True:
    fields = input("Enter a list of fields to keep (e.g., '[\"name\", \"age\"]'): \n\t -a [all fields] \n" + '-'*50 + "\n" + "Choice: ").strip()

    # if user puts "a", use all fields 
    if fields == 'a':
        fields = str(columns).replace("'", "\"")
    try:
        fields_check = json.loads(fields)
        if isinstance(fields_check, list):
            if all([(field in columns) for field in json.loads(fields)]):
                break
            else:
                print(f"Some of the fields you entered are not in {outfile}. Please try again.")

        else:
            print("Incorrect format. Please use json list (e.g., '[\"name\", \"age\"]')")
    except json.JSONDecodeError:
        print("Incorrect format. Please use json list (e.g., '[\"name\", \"age\"]')")




##############################################################################################################################

## Check if json files are unpacked.  ##
# If not, unpack using tsvtojson and repackage.py

json_dir = os.path.join(parent_dir, "json")

if os.path.isdir(json_dir) and any(f.endswith(".json") for f in os.listdir(json_dir)):
    json_count = sum(1 for f in os.listdir(json_dir) if f.endswith(".json"))
    print("\n" + "-"*50, "You have already unpacked the haunted place json files", f"Total Json count: {json_count}", "Skipping unpacking using 'tsvtojson' and 'repackage.py'.", sep = "\n", end = "\n" + "-"*50)
else:
    ##############################################################################################################################
    ## Run tsvtojson and repackage ##
    print("\n" + "-"*50, "Unpacking haunted places dataset using 'tsvtojson' and 'repackage.py'", "Jsons stored in ./data/tika_similarity/json/*", "Aggregate_json stored in ./data/tika_similarity/aggregate_json/aggregate.json", sep = "\n", end = "\n" + "-"*50)
    ## Read CSV and save copy with no header for tsvtojson ##
    
    outfile = "./data/processed/haunted_places_features_added.tab"

    df = pd.read_csv(outfile, sep="\t")  

    df.to_csv(outfile.replace("added", "added_nh"), index = False, header = False, sep = "\t")


    ## column_headers.conf ##

    with open("./data/tika_similarity/conf/col_headers.conf", "w") as f:
        f.write("\n".join(df.columns.tolist()))
        f.close()

    ## encoding.conf ##

    supported_text_encodings = ['utf-8', 'us-asci'] 

    with open("./data/tika_similarity/conf/encoding.conf", "w") as f:
        f.write("\n".join(supported_text_encodings))
        f.close()
        
    ##############################################################################################################################

    ## Run tsvtojson ##

    command = [
        "tsvtojson",
        "-t", outfile.replace("added", "added_nh"),
        "-j", "./data/tika_similarity/aggregate_json/aggregate.json",
        "-c", "./data/tika_similarity/conf/col_headers.conf",
        "-o", "hauntedPlaces",
        "-e", "./data/tika_similarity/conf/encoding.conf",
        "-s", "0.8",
        "-v"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Remove temporary dataframe with no headers
    os.remove(outfile.replace("added", "added_nh"))

    ##############################################################################################################################

    ## Run repackage ##

    # Move to json directory #
    json_dir = "./data/tika_similarity/json"
    os.chdir(json_dir)

    # Run command #
    command = [
        "repackage",
        "-j", "../aggregate_json/aggregate.json",
        "-o", "hauntedPlaces", "-v"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    print("Jsons stored in './tika_similarity/json' and are ready for clustering")

##############################################################################################################################
## Get Similarity Scores ##

## Run clusterHelper.py to get [method].csv ##
print("\nNow running ./dsci_550_a1/clusterHelper.py:", end = "\n\n")
## Move back into project directory ##
os.chdir(starting_dir)

helper_output = os.path.join(clustering_subdir, f"{clustering_method}.csv")

command = [
    "python", "./dsci_550_a1/clusterHelper.py",
    "--input_dir", "./data/tika_similarity/json",
    "--subset_dir", "./data/tika_similarity/temp",
    "--num_files", num_files, 
    "--out_csv", helper_output,
    "--fields", fields,
    "--method", cluster_char
]


result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

# Replace '/temp/' with '/json/' in helper_output #
df2 = pd.read_csv(helper_output, sep = ",")
df2['x-coordinate'] = df2['x-coordinate'].apply(lambda x: x.replace("/temp/", "/json/"))
df2['y-coordinate'] = df2['y-coordinate'].apply(lambda x: x.replace("/temp/", "/json/"))
df2.to_csv(helper_output, sep = ",", index = False) 

##############################################################################################################################

command = [
    "python", "./clones/tika-img-similarity/tikasimilarity/cluster/edit-cosine-circle-packing.py",
    "--inputCSV", f"{helper_output}",
    "--cluster", circle_packing_kwarg,
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

    
command = [
    "python", "./clones/tika-img-similarity/tikasimilarity/cluster/edit-cosine-cluster.py",
    "--inputCSV", f"{helper_output}",
    "--cluster", "2",
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

command = [
    "python", "./clones/tika-img-similarity/tikasimilarity/cluster/generateLevelCluster.py",
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

##############################################################################################################################
## Make HTML ##

command = "cp -R ./clones/etllib/html/* ."

result = subprocess.run(command, shell = True, capture_output=True, text=True)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)


##############################################################################################################################
## Save Metadata and move outputs ##

# Metadata
metadata_filepath = os.path.join(clustering_subdir, "metadata.json")
print("\n" + "-"*50, f"Metadata saved to {metadata_filepath}", sep = "\n", end = "\n\n")

metadata = {
    "number of files" : len(num_files) if isinstance(num_files, list) else num_files,
    "haunted place indicies" : num_files if isinstance(num_files, list) else 'random sample', 
    "fields" : fields,
    "input_data" : outfile, 
    "method" : clustering_method
}

with open(metadata_filepath, "w") as f:
    json.dump(metadata, f, indent = 4)


# Output directory
output_dir = os.path.join(clustering_subdir, "visualization")
os.makedirs(os.path.join(output_dir), exist_ok = True)

print(f"Moving output files to {output_dir}", end = "\n\n")


output_html = ['./circlepacking.html', 'cluster-d3.html', 'levelCluster-d3.html']
output_json = ['circle.json', 'levelCluster.json', 'clusters.json']



for file in output_html:
    dest_path = os.path.join(output_dir,os.path.basename(file))
    shutil.move(file, dest_path)

for file in output_json:
    dest_path = os.path.join(output_dir,os.path.basename(file))
    shutil.move(file, dest_path)
    
print("All Done :)", "\n" + "-"*50, sep = "\n")


