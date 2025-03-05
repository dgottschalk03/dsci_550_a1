import pandas as pd

# Paths
input_file = "data/processed/haunted_places_with_new_columns.csv"
target_file = "data/processed/haunted_places_features_added.tab"

# Read the CSV with new columns
new_columns_df = pd.read_csv(input_file)

# Read the existing target file
try:
    target_df = pd.read_csv(target_file, sep="\t")
    print(f"Updating existing file: {target_file}")
except FileNotFoundError:
    print(f"Target file not found. Creating new file.")
    target_df = new_columns_df.copy()

# Get the new columns to add
new_feature_names = ["Daylight_Duration_Hours", "Data_Source"]

# Add or update the new columns
for feature in new_feature_names:
    if feature in new_columns_df.columns:
        print(f"Adding/updating column: {feature}")
        target_df[feature] = new_columns_df[feature]
    else:
        print(f"Warning: Column {feature} not found in source file")

# Save the updated dataframe
target_df.to_csv(target_file, sep="\t", index=False)
print(f"CSV saved to {target_file}")