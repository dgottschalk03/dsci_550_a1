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

## Create clustering output directory ##
if not os.path.exists("./clustering"):
    os.makedirs("./clustering")

if not os.path.exists("./clustering/jaccard"):
    os.makedirs("./clustering/jaccard")


## Create directories for aggregate.json, json, and conf files  in data folder ##

parent_dir = "./data/tika_similarity"
child_dirs = ["aggregate_json", "conf", "json", "temp", "clusters"]

os.makedirs(parent_dir, exist_ok = True)
for child in child_dirs:
    os.makedirs(os.path.join(parent_dir, child), exist_ok = True)


##############################################################################################################################

## User input ##
# user inputs fields tocluster by and number of files they wish to cluster


outfile = "./data/processed/haunted_places_features_added.tab"
columns = pd.read_csv(outfile, nrows = 0, sep = "\t").columns.tolist()

## Subset of files you want to cluster ##
num_files = '' 
while not num_files.isdigit() or not (0 < int(num_files) <= 10992):
    num_files = input("Enter number of haunted places to cluster: ")

num_files = num_files

## subset of fields you want to consider
fields = ''
while True:
    fields = input("Enter a list of fields to keep (e.g., '[\"name\", \"age\"]'): ").strip()

    try:
        fields_check = json.loads(fields)
        if isinstance(fields_check, list):
            if all([(field in columns) for field in json.loads(fields)]):
                break
            else:
                print("Some of the fields you entered are not in {outfile}. Please try again.")

        else:
            print("Incorrect format. Please use json list (e.g., '[\"name\", \"age\"]')")
    except json.JSONDecodeError:
        print("Incorrect format. Please use json list (e.g., '[\"name\", \"age\"]')")



# ## Create clustering output directory ##
# if not os.path.exists("./clustering"):
#     os.makedirs("./clustering")

# if not os.path.exists("./clustering/jaccard"):
#     os.makedirs("./clustering/jaccard")


# ## Create directories for aggregate.json, json, and conf files  in data folder ##

# parent_dir = "./data/tika_similarity"
# child_dirs = ["aggregate_json", "conf", "json", "temp", "clusters"]

# os.makedirs(parent_dir, exist_ok = True)
# for child in child_dirs:
#     os.makedirs(os.path.join(parent_dir, child), exist_ok = True)

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

## Run jaccardSimilarity.py to get jaccard.csv ##
print("\nNow running ./dsci_550_a1/runJaccardSimilarity.py:", end = "\n\n")
## Move back into project directory ##
os.chdir(starting_dir)


command = [
    "python", "./dsci_550_a1/runJaccardSimilarity.py",
    "--input_dir", "./data/tika_similarity/json",
    "--subset_dir", "./data/tika_similarity/temp",
    "--num_files", num_files, 
    "--out_csv", "./clustering/jaccard/jaccard.csv",
    "--fields", fields
]


result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

# Replace '/temp/' with '/json/' in jaccard.csv #
df2 = pd.read_csv("./clustering/jaccard/jaccard.csv", sep = ",")
df2['x-coordinate'] = df2['x-coordinate'].apply(lambda x: x.replace("/temp/", "/json/"))
df2['y-coordinate'] = df2['y-coordinate'].apply(lambda x: x.replace("/temp/", "/json/"))
df2.to_csv("./clustering/jaccard/jaccard.csv", sep = ",", index = False) 

##############################################################################################################################

## Run 'edit-cosine-circle-packing.py' 'edit-cosine-cluster.py' and 'generateLevelCluster.py' ##

command = [
    "python", "./clones/tika-img-similarity/tikasimilarity/cluster/edit-cosine-circle-packing.py",
    "--inputCSV", "./clustering/jaccard/jaccard.csv",
    "--cluster", "2",
]

result = subprocess.run(command, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)


command = [
    "python", "./clones/tika-img-similarity/tikasimilarity/cluster/edit-cosine-cluster.py",
    "--inputCSV", "./clustering/jaccard/jaccard.csv",
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

print("\n" + "-"*50, "Metadata saved to ./clustering/jaccard/metadata.json", sep = "\n", end = "\n\n")

metadata = {
    "num_files" : num_files,
    "fields" : fields,
    "input_data" : outfile
}

with open("./clustering/jaccard/metadata.json", "w") as f:
    json.dump(metadata, f, indent = 4)

print("Moving output files to ./clustering/jaccard/visualization", end = "\n\n")

output_dir = "./clustering/jaccard"
output_html = ['./circlepacking.html', 'cluster-d3.html', 'levelCluster-d3.html']
output_json = ['circle.json', 'levelCluster.json', 'clusters.json']

output_viz = os.path.join(output_dir, "visualization")
os.makedirs(os.path.join(output_viz), exist_ok = True)


for file in output_html:
    dest_path = os.path.join(output_viz,os.path.basename(file))
    shutil.move(file, dest_path)

for file in output_json:
    dest_path = os.path.join(output_viz,os.path.basename(file))
    shutil.move(file, dest_path)
    
print("All Done :)", "\n" + "-"*50, sep = "\n")


