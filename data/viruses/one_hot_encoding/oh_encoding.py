import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def main():
    virus_traits_df = pd.read_csv("finished_traits/cleaned/virus_traits.csv")
    
    categorical_cols = ["Order", "Family","Genus","envelope","circular",
    "double_stranded","rna","segmented","positive_sense",
    "negative_sense","budding","lysis",
    "release_other","cytoplasm","CE_clathrin","CE_receptor",
    "CE_glycoproteins","CE_other"]

    encoder = OneHotEncoder(sparse_output=False)

    one_hot_encoded = encoder.fit_transform(virus_traits_df[categorical_cols])
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_cols))

    processed_df = pd.concat([virus_traits_df, one_hot_encoded_df], axis=1)

    processed_df = processed_df.drop(categorical_cols, axis=1)

    processed_df.to_csv("virus_traits_processed.csv", index=False)


if __name__ == "__main__":
    main()