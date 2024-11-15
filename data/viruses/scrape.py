import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

viral_zone_url = "https://viralzone.expasy.org"

#search virus in search bar
#should never return error
def search_virus(virus_name):
    print(virus_name)
    search_url = f"{viral_zone_url}/search?query={virus_name.replace(' ', '+')}"

    response = requests.get(search_url)
    if response.status_code == 200:
        return response.text
    else:
        # print("Error fetching search results.")
        return None

#parse search results looking for associated viruses link
def get_virus_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    virus_link = None

    try:
        rows = soup.find('table', class_='catalog').find_all('tr')
        # link = base_url+ soup.find('table', class_='catalog').find('a')['href']
        for row in rows:
            associated_span = row.find('span', class_='notice3')
            if associated_span and "Associated names" in associated_span.get_text():
                a_tag = row.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    virus_link = viral_zone_url+ a_tag['href']
                    print("Href attribute for the first row with 'Associated names':", virus_link)
                break
        else:
            print("No Assoc rows")
    except:
        print("Page not found")

    return virus_link


def get_virus_page(link):
    if link:
        print(link)
        # try:
        response = requests.get(link)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print("Error fetching virus page.")
            return None
    else:
        print("Bad link")
        return None


def check_replication_in_cytoplasm(soup):
    cyto = ["CYTOPLASM", "CYTOPLASMIC"]

    strongs = soup.find_all('strong')
    for strong in strongs:
        text = strong.get_text()
        if text in cyto:
            print("YES cyto")
            return 1
    else:
        print("NO cyto")
        return "0" 


def find_trait(virus_name, search_func, seen):
    # print(seen)
    if virus_name in seen:
        return seen[virus_name]
    else:
        search_results = search_virus(virus_name)
        if not search_results:
            print("Error fetching search results.")
            seen[virus_name] = 2
            return seen[virus_name]

        virus_link = get_virus_link(search_results)
        if not virus_link:
            print("No Associated names page")
            seen[virus_name]=  3
            return seen[virus_name]

        page_html = get_virus_page(virus_link)
        if not page_html:
            print("Could not fetch virus page")
            seen[virus_name] = 4
            return seen[virus_name]
        
        seen[virus_name] = search_func(page_html)
    
    return seen[virus_name]

    
def get_cyto(infile, outfile, level, col):
    df = pd.read_csv(infile)
 
    df[f"cytoplasm_{level}"] = df[col].apply(lambda name: find_trait(str(name), check_replication_in_cytoplasm) or 'Not found')
    df.to_csv(outfile, index=False)

def get_cyto_manual():
    cyto_dict = {
        "Picornavirales" : 1,
        "Reovirales": 1,
        "Herpesvirales": 0,
        "Tolivirales": 1,
    }

    def manual(name):
        if name in cyto_dict.keys():
            return cyto_dict[name]
        else:
            return 3

    df = pd.read_csv("missing_cyto_family.csv")
    df[f"cytoplasm_order"] = df["Order"].apply(lambda name: manual(name))
    df.to_csv("cytoplasm_order", index=False)
    df = df[df.cytoplasm_genus > 1]
    df = df[df.cytoplasm_family > 1]
    df = df[df.cytoplasm_order > 1]
    df.to_csv("missing_cyto_order", index=False)

def merge_cyto():
    df1 = pd.read_csv("cyto_species.csv")
    df2 = pd.read_csv("cyto_genus.csv")
    df2.drop(columns=["NCBI Taxon ID", "Order", "Family", "Genus", "cytoplasm_species"], inplace=True)
    
    df3 = pd.read_csv("cyto_family.csv")  # Assuming this is df3
    df3.drop(columns=["NCBI Taxon ID", "Order", "Family", "Genus", "cytoplasm_species", "cytoplasm_genus"], inplace=True)
    
    df4 = pd.read_csv("cyto_order.csv")
    df4.drop(columns=["NCBI Taxon ID", "Order", "Family", "Genus", "cytoplasm_species", "cytoplasm_family", "cytoplasm_genus"], inplace=True)


    # Merge the DataFrames one by one, and drop duplicate columns
    merged_df = pd.merge(df1, df2, on='Species', how='outer', suffixes=('_df1', '_df2'))
    # columns_to_drop = [col for col in merged_df.columns if col.endswith('_df1')]
    # merged_df.drop(columns=columns_to_drop, inplace=True)

    merged_df = pd.merge(merged_df, df3, on='Species', how='outer', suffixes=('_df2', '_df3'))
    # columns_to_drop = [col for col in merged_df.columns if col.endswith('_df2')]
    # merged_df.drop(columns=columns_to_drop, inplace=True)

    merged_df = pd.merge(merged_df, df4, on='Species', how='outer', suffixes=('_df3', '_df4'))
    # columns_to_drop = [col for col in merged_df.columns if col.endswith('_df3')]
    # merged_df.drop(columns=columns_to_drop, inplace=True)

    # Drop 'Unnamed: 0' column if it exists
    merged_df.drop(columns=["Unnamed: 0_df3", "Unnamed: 0.1", "Unnamed: 0_df4"], inplace=True, errors='ignore')

    
    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('merged_output.csv', index=False)

def agg_cyto():
    df = pd.read_csv("merged_output.csv")
    def calc_val(row):
        for col in ['cytoplasm_species', 'cytoplasm_genus', 'cytoplasm_family', 'cytoplasm_order']:
            if pd.notnull(row[col]) and row[col] != 3:
                return int(row[col])
        return 2

    df['cytoplasm'] = df.apply(calc_val, axis=1)
    df.drop(columns=['cytoplasm_species', 'cytoplasm_genus', 'cytoplasm_family', 'cytoplasm_order'], inplace=True)

    df.to_csv('updated_file.csv', index=False)

    

    print("New 'cytoplasm' column added.")

if __name__ == "__main__":
    # print(check_replication_in_cytoplasm(parse_search_results(search_virus(str("Paslahepevirus balayani")))))
    # get_cyto("missing_cyto_family.csv", "cyto_order.csv", "order", "Order")
    # merge_cyto()
    agg_cyto()
    # df = pd.read_csv("missing_cyto_family.csv")
    # df = df[df.cytoplasm_species >1]
    # df = df[df.cytoplasm_genus > 1]
    # df = df[df.cytoplasm_family > 1]
    # df = df.groupby(["Order"]).sum()
    # df.to_csv("family.csv")

