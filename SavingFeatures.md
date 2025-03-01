# Loading Data and Saving Features

## Preamble code
    ## Copy this code into your preamble. 

    # Output Df
    outfile = "../data/processed/haunted_places_features_added.tab"

    # Reading CSV
    df = pd.read_csv("../data/processed/haunted_places_cleaned.tab", sep = "\t")

    # Feature Names
    feature_names = ["Audio_Evidence"]

## Put this at the end of your program to save features added
    ## Save CSV ##
    print("Saving to CSV...")

    # Read Feature added dataframe
    out_df = pd.read_csv(f"{outfile}", sep = "\t")


    # Check if feature exists
    for feature in feature_names:
        
        # If it exists, update values
        if feature in out_df.columns:
            out_df[feature].update(df[feature].values)
            out_df[feature] = df[feature].values

        # If not add entire column
        else:
            out_df[feature] = df[feature].values

    out_df.to_csv(f"{outfile}", sep = "\t", index = False)

    print(f"CSV Saved to {outfile}")
