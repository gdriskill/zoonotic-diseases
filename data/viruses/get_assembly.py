import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import os
from xml.etree import ElementTree as ET
import json
    

# from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# os.environ['PYPPETEER_CHROMIUM_EXECUTABLE'] = '/snap/bin/chromium'

def get_species_lineage_assembly():
    df = pd.read_csv("../interactions/NCBI/interactions-assembly.csv")
    grouped = df.drop(["Pathogen Organism Name","Host","Total Count","GenBank Count","RefSeq Count","Completed Count"], axis=1, inplace=True)
    grouped = df.groupby("Pathogen Species")['Assembly'].agg(list)
    grouped.to_csv("species_assembly.csv")

def get_GA(arr):
    for item in arr:
        if item:
            return item
    return 0

def clean_assembly():
    df = pd.read_csv("../interactions/NCBI/interactions-assembly.csv")
    df['Assembly'] = df['Assembly'].astype(str)
    df['Assembly'] = df['Assembly'].apply(lambda x: 0 if x.startswith("set:") else x)
    grouped = df.groupby("Pathogen Species")["Assembly"].agg(list).reset_index()

    grouped["GA"] = grouped["Assembly"].apply(get_GA)
    grouped = grouped.drop("Assembly", axis=1)

    grouped.to_csv("cleaned_species_assembly.csv", index=False)

def assembly_lookup(species, data):
    for case in data:
        if case["species"] == species:
            return case["GA"]
    return 0

def add_missing_assemblies():
    with open("data.json", 'r') as f:
        data = json.load(f)

        df = pd.read_csv("cleaned_species_assembly.csv")
        df["GA"] = df["GA"].astype(str)
        df["GA"] = df.apply(lambda row: assembly_lookup(row["Pathogen Species"], data) if not row["GA"].startswith("GC") else row["GA"], axis=1)
        df.to_csv("updated_species_assembly.csv", index=False)

def genome_stats_lookup(species, data):
    for case in data:
        # print(case)
        if case["species"] == species:
            case["size"] = int(case["size"].replace(",", ""))
            return case
    return {
        "species": species,
        "GA": None,
        "size": None,
        "gc": None,
        "genes": None
    }

def add_gene_stats():
    with open("genome_stats.json", 'r') as f:
        data = json.load(f)

        df = pd.read_csv("cleaned_species_assembly.csv")
         
        df[f"result"] = df["Pathogen Species"].apply(lambda name: genome_stats_lookup(str(name), data))
        dict_cols = pd.json_normalize(df['result'])

        df = pd.concat([df, dict_cols], axis=1)

        df.drop(columns=['result'], inplace=True)

        df.to_csv("final_gene_stats.csv", index=False)


if __name__ == "__main__":
    # get_species_lineage_assembly()
    # clean_assembly()
    # add_missing_assemblies()
    add_gene_stats()
    # test()
    
