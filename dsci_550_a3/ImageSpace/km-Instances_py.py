import csv
import requests
import json

# Path to your color_clustering.csv file
csv_file_path = '/Users/kater/output_folder/color_clustering.csv'

# URL of your running ElasticSearch instance
es_url = 'http://localhost:9200/imagespace/_doc/'  # "imagespace" is your index name

# Open and read the CSV
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Prepare the document
        doc = {
            "image_name": row['Image'],
            "cluster_id": int(row['Cluster'])
        }
        
        # Send to ElasticSearch
        response = requests.post(es_url, headers={"Content-Type": "application/json"}, data=json.dumps(doc))
        
        # Print the response
        print(response.status_code, response.text)
