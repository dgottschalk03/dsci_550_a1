import json
from collections import defaultdict
import os


def unpack_cluster(file_path):
    

    with open(file_path, "r") as f:
        data = json.load(f)

    clusters = defaultdict(list)

    # Read cluster data
    for cl in data.get("children", []):
        
        # Init cluster dict
        clusters[cl['name']] = []

        # Read each haunted place
        for entry in cl.get("children", []):

            # Check if current directory in dsci_550_a1
            starting_dir = os.getcwd()

            # If it doesn't end with dsci_550_a1, try going up and finding project dir
            if not starting_dir.endswith("dsci_550_a1"):
                try:
                    # If project dir found, construct relative path
                    idx = starting_dir.split("/").index("dsci_550_a1")
                    project_dir = ("/".join(starting_dir.split("/")[:idx+1]) + "/")

                # If project dir not found ... scold user and exit
                except ValueError:
                    print("Please run this module from within the dsci_550_a1 directory")

            # Open Json
            with open(project_dir + entry['name'].split()[0][1:], 'r') as haunted_place:

                # Extract index and add to output
                idx = int(json.load(haunted_place)["Haunted_Places_Id"])
                clusters[cl['name']].append(idx)

    os.chdir(starting_dir)
    
    return clusters
