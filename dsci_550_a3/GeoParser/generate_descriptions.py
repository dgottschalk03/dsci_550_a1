import pandas as pd

df = pd.read_csv('../data/raw/haunted_places.tab', sep='\t')


print("Columns in dataset:", df.columns.tolist())

# Make sure required columns exist
if 'location' not in df.columns or 'description' not in df.columns:
    raise ValueError("Missing 'location' or 'description' column.")

df['text'] = df.apply(
    lambda row: f"{row['location']} is known for: {row['description']}", axis=1
)


df[['text']].to_csv('haunted_descriptions.csv', index=False)

print("Descriptions saved to haunted_descriptions.csv")


