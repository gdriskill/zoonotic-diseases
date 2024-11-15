import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


def get_species_lineage_assembly():
    df = pd.read_csv("interactions-assembly.csv")
    grouped = df.drop(["Pathogen Organism Name","Host","Total Count","GenBank Count","RefSeq Count","Completed Count"], axis=1, inplace=True)
    grouped = df.groupby("Pathogen Species")['Assembly'].agg(list).reset_index()
    grouped.to_csv("species_assembly.csv")

if __name__ == "__main__":
    get_species_lineage_assembly()
