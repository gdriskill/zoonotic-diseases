import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

base_url = "https://viralzone.expasy.org"

# Function to search for a virus
def search_virus(virus_name):
    print(virus_name)
    search_url = f"{base_url}/search?query={virus_name.replace(' ', '+')}"
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching search results.")
        return None
    
def parse_search_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    link = None

    try:
        rows = soup.find('table', class_='catalog').find_all('tr')
        # link = base_url+ soup.find('table', class_='catalog').find('a')['href']
        for row in rows:
            associated_span = row.find('span', class_='notice3')
            if associated_span and "Associated names" in associated_span.get_text():
                a_tag = row.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    link = base_url+ a_tag['href']
                    print("Href attribute for the first row with 'Associated names':", link)
                break
        else:
            print("No assoc rows")
    except:
        print("not found")

    return link

def get_virus_page(virus_page_url):
    if virus_page_url:
        print(virus_page_url)
        # try:
        response = requests.get(virus_page_url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print("Error fetching virus page.")
            return 3
    else:
        print("bad page")
        return 4


def check_replication_in_cytoplasm(virus_page_url):
    cyto = ["CYTOPLASM", "CYTOPLASMIC"]
    soup = get_virus_page(virus_page_url)

    strongs = soup.find_all('strong')
    for strong in strongs:
        text = strong.get_text()
        if text in cyto:
            print("yes cyto")
            return 1
    else:
        print("no cyto")
        return "0" 
    
def get_cyto():
    df = pd.read_csv(f"species_lineage.csv")
 
    df["cytoplasm_genus"] = df["Genus"].apply(lambda name: check_replication_in_cytoplasm(parse_search_results(search_virus(str(name)))) or 'Not found')
    df.to_csv(f"cyto_genus.csv", index=False)

if __name__ == "__main__":
    # print(check_replication_in_cytoplasm(parse_search_results(search_virus(str("Paslahepevirus balayani")))))
    get_cyto()

