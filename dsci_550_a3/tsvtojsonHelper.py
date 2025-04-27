# System Path #
import os
import sys 
import shutil
import subprocess
import pandas as pd
import subprocess
import json
import datetime

## Create directories for aggregate.json, json, and conf files in data folder ##

parent_dir = "./data/d3"
child_dirs = ["aggregate_json", "conf"] # ["aggregate_json", "conf", "json", "temp"]

os.makedirs(parent_dir, exist_ok = True)
for child in child_dirs:
    os.makedirs(os.path.join(parent_dir, child), exist_ok = True)

json_dir = os.path.join(parent_dir, "json")

## Check if jsons are already inpacked

if os.path.isdir(json_dir) and any(f.endswith(".json") for f in os.listdir(json_dir)):
    json_count = sum(1 for f in os.listdir(json_dir) if f.endswith(".json"))
    print("\n" + "-"*50, "You have already unpacked the haunted place json files", f"Total Json count: {json_count}", "Do you want to wipe and run 'tsvtojson' and 'repackage.py'?", sep = "\n", end = "\n" + "-"*50)

userInput = ""
while userInput != "y" and userInput != "n":
    userInput = input("Do you want to proceed? (y/n): ").lower()
    if userInput == "y":
        print("\n" + "-"*50, "Running 'tsvtojson' and 'repackage.py'", sep = "\n", end = "\n" + "-"*50 + "\n")
    elif userInput == "n":
        print("\n" + "-"*50, "Skipping 'tsvtojson' and 'repackage.py'", "Goodbye!", sep = "\n", end = "\n" + "-"*50 + "\n")
        sys.exit()

##############################################################################################################################
## Wipe Directory ##

for child in child_dirs:
    dir_path = os.path.join(parent_dir, child)
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) 
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"Cleared contents of: {dir_path}")
    else:
        print(f"Directory does not exist: {dir_path}")

##############################################################################################################################
## Run tsvtojson and repackage ##

print("\n" + "-"*50, "Unpacking haunted places dataset using 'tsvtojson' and 'repackage.py'", "Jsons stored in ./data/tika_similarity/json/*", "Aggregate_json stored in ./data/tika_similarity/aggregate_json/aggregate.json", sep = "\n", end = "\n" + "-"*50)
## Read CSV and save copy with no header for tsvtojson ##

outfile = "./data/processed/haunted_places_features_added_v2.tab"

df = pd.read_csv(outfile, sep="\t")  

df.to_csv(outfile.replace("added", "added_nh"), index = False, header = False, sep = "\t")


## column_headers.conf ##

with open(f"{parent_dir}/conf/col_headers.conf", "w") as f:
    f.write("\n".join(df.columns.tolist()))
    f.close()

## encoding.conf ##

supported_text_encodings = ['utf-8', 'us-asci'] 

with open(f"{parent_dir}/conf/encoding.conf", "w") as f:
    f.write("\n".join(supported_text_encodings))
    f.close()
    
##############################################################################################################################
## Run tsvtojson ##

command = [
    "tsvtojson",
    "-t", outfile.replace("added", "added_nh"),
    "-j", f"{parent_dir}/aggregate_json/aggregate.json",
    "-c", f"{parent_dir}/conf/col_headers.conf",
    "-o", "hauntedPlaces",
    "-e", f"{parent_dir}/conf/encoding.conf",
    "-s", "0.8",
    "-v"
]

result = subprocess.run(command, capture_output=True, text=True)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

# Remove temporary dataframe with no headers
os.remove(outfile.replace("added", "added_nh"))

##############################################################################################################################
## convert datetime strings into datetime objects ##

with open(f"{parent_dir}/aggregate_json/aggregate.json", "r") as f:
    data = json.load(f)
    
    data_sorted = sorted(data['hauntedPlaces'], key = lambda x : int(x['Haunted_Places_Id']))
    for entry in data_sorted:
        entry["Haunted_Places_Date"] = eval(entry["Haunted_Places_Date"])
        entry["Haunted_Places_Date"] = [date.isoformat() for date in entry["Haunted_Places_Date"] if isinstance(date, datetime.date)]

with open(f"{parent_dir}/aggregate_json/aggregate.json", "w") as f:
    json.dump(data, f, indent=4)

##############################################################################################################################
## Run repackage ##

# Move to json directory #


# json_dir = f"{parent_dir}/json"
# os.chdir(json_dir)

# # Run command #
# command = [
#     "repackage",
#     "-j", "../aggregate_json/aggregate.json",
#     "-o", "hauntedPlaces", "-v"
# ]

# result = subprocess.run(command, capture_output=True, text=True)
# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)

# print(f"Jsons stored in '{parent_dir}/json'")