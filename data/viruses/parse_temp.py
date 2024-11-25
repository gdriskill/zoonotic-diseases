import pandas as pd
import requests
import time


def get_strain(s, separator):
    vals = s.split(separator)
    print(vals)
    return " ".join(vals[:-1])

def get_ncbi_taxid(virus_name):

    print(virus_name)
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "taxonomy",      
        "term": virus_name,     
        "retmode": "json",       
    }

        # Send request to NCBI API
    response = requests.get(base_url, params=params)
    time.sleep(0.5)
    if response.status_code == 200:
        data = response.json()
        # Check if any ID is returned in the results
        if data['esearchresult']['idlist']:
            taxid = data['esearchresult']['idlist'][0]  # Take the first match
            if (len(data['esearchresult']['idlist']) > 1):
                print(virus_name)
            return taxid
        else:
            print("No TaxID found for:", virus_name)
            return None
    else:
        print("Error:", response.status_code, virus_name)
        return None

def get_taxonomic_info(taxid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "taxonomy",
        "id": taxid,
        "retmode": "xml",
    }
    time.sleep(0.5)
    response = requests.get(base_url, params=params)
    data = response.text
    print(taxid)

    # Parse the XML response manually to find Order, Family, and Genus
    tax_info = {"Order": None, "Family": None, "Genus": None}
    if "<LineageEx>" in data:
        lineage_start = data.index("<LineageEx>") + len("<LineageEx>")
        lineage_end = data.index("</LineageEx>")
        lineage_xml = data[lineage_start:lineage_end]
        
        # Loop through the lineage to find the ranks
        for rank in tax_info.keys():
            if f"<Rank>{rank.lower()}</Rank>" in lineage_xml:
                rank_index = lineage_xml.index(f"<Rank>{rank.lower()}</Rank>")
                sci_name_start = lineage_xml.rfind("<ScientificName>", 0, rank_index) + len("<ScientificName>")
                sci_name_end = lineage_xml.index("</ScientificName>", sci_name_start)
                tax_info[rank] = lineage_xml[sci_name_start:sci_name_end]
                
    return tax_info



def get_viruses(level="organism"):
    df = pd.read_csv("interactions-species.csv")
    virus_df = df[["Species"]].drop_duplicates()
    virus_df.to_csv(f"species_all.csv", index=False)


def get_taxid(level="species"):
    filter_column="Species"
    df = pd.read_csv(f"species.csv")
    df["NCBI Taxon ID"] = df[filter_column].apply(lambda name: get_ncbi_taxid(name) or 'Not found')
    df.to_csv(f"{level}_taxid.csv", index=False)

def get_lineage(level="species"):
    df = pd.read_csv(f"{level}_taxid.csv")

    taxonomy_data = df["NCBI Taxon ID"].apply(lambda name: get_taxonomic_info(name) or 'Not found')
    df = pd.concat([df, taxonomy_data.apply(pd.Series)], axis=1)
    df.to_csv(f"{level}_lineage.csv", index=False)

if __name__ == "__main__":

    # get_viruses()
    # get_taxid()
    get_lineage()


