import pandas as pd

def prepare_full_traits():
    df = pd.read_csv("combined_output.csv")
    df.drop(columns=["GA"], inplace=True)
    df.fillna(0, inplace=True)

    df.to_csv("virus_traits_all-OHE.csv",index=False)

def prepare_cat_traits():
    df = pd.read_csv("virus_traits_all-OHE.csv")
    df.drop(columns=["size", "gc", "genes", "size_missing", "gc_missing", "genes_missing"], inplace=True)
    df.to_csv("virus_traits_cat-OHE.csv", index=False)

if __name__ == "__main__":
    prepare_full_traits()
    prepare_cat_traits()