import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def main():
    bird_traits_df = pd.read_csv("birds_traits.csv", index_col=0)
    
    categorical_cols = ["order","family","trophic level","trophic niche","primary lifestyle","habitat"]

    # drop unneeded columns
    bird_traits_df = bird_traits_df.drop(["scientific name", "alternative name"], axis=1)

    # Create an encoder
    encoder = OneHotEncoder(sparse_output=False)

    # Apply encoder and make df of encoded columns
    one_hot_encoded = encoder.fit_transform(bird_traits_df[categorical_cols])
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_cols))

    # Combine encoded columns and original
    processed_df = pd.concat([bird_traits_df, one_hot_encoded_df], axis=1)

    # drop the unencoded categorical columns
    processed_df = processed_df.drop(categorical_cols, axis=1)

    # Save the processed dataframe
    processed_df.to_csv("birds_traits_processed.csv")


if __name__ == "__main__":
    main()