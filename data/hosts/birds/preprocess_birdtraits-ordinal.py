import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

def main():
    bird_traits_df = pd.read_csv("birds_traits.csv", index_col=0)
    
    categorical_cols = ["order","family","trophic level","trophic niche","primary lifestyle","habitat"]

    # drop unneeded columns
    bird_traits_df = bird_traits_df.drop(["scientific name", "alternative name"], axis=1)

    # Create an encoder
    encoder = OrdinalEncoder()

    # Apply encoder and add encoded columns to df
    encoder.fit(bird_traits_df[categorical_cols])
    bird_traits_df[categorical_cols] = encoder.transform(bird_traits_df[categorical_cols])

    # Save the processed dataframe
    bird_traits_df.to_csv("birds_traits_processed-ordinal.csv")


if __name__ == "__main__":
    main()