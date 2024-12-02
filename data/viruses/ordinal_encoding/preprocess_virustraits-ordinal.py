import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

def main():
    virus_traits_df = pd.read_csv("finished_traits/cleaned/virus_traits.csv")
    
    categorical_cols = ["Order","Family","Genus",
                        "envelope","circular","double_stranded","rna","segmented",
                        "positive_sense","negative_sense","budding","lysis","release_other","cytoplasm","CE_clathrin",
                        "CE_receptor","CE_glycoproteins",'CE_other']

    # drop unneeded columns
    virus_traits_df = virus_traits_df.drop(["Unnamed: 0"], axis=1)

    # Create an encoder
    encoder = OrdinalEncoder()

    # Apply encoder and add encoded columns to df
    encoder.fit(virus_traits_df[categorical_cols])
    virus_traits_df[categorical_cols] = encoder.transform(virus_traits_df[categorical_cols])

    # Save the processed dataframe
    virus_traits_df.to_csv("virus_traits_processed-ordinal.csv")


if __name__ == "__main__":
    main()