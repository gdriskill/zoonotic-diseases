import pandas as pd
from scrape import *


def check_entry(text, gene_dict):
    # print(text)
    if "clathrin" in text:
            gene_dict['CE_clathrin']= 1
            gene_dict['CE_receptor']= 0
            gene_dict['CE_glycoproteins']= 0
            gene_dict['other']= 0
    
    if "glycoprotein" in text:
        gene_dict['CE_clathrin']= 0
        gene_dict['CE_receptor']= 0
        gene_dict['CE_glycoproteins']= 1
        gene_dict['other']= 0

    if "attachement of viral proteins" in text:
        gene_dict['CE_clathrin']= 0
        gene_dict['CE_receptor']= 1
        gene_dict['CE_glycoproteins']= 0
        gene_dict['other']= 0

    if "host receptors" in text:
        gene_dict['CE_clathrin']= 0
        gene_dict['CE_receptor']= 1
        gene_dict['CE_glycoproteins']= 0
        gene_dict['other']= 0
    
    return gene_dict
    

def check_entry_in_html(soup):
    ps = soup.find_all("p")

    gene_dict = {
        'CE_clathrin': 2,
        'CE_receptor':2,
        'CE_glycoproteins':2,
        'other':2,
        "finished": 0,
    }
    
    for p in ps:
        text = p.get_text()
        text = text.lower()

        gene_dict = check_entry(text, gene_dict)

    li_tags = soup.find_all("li")

    for li in li_tags:
        text = li.get_text()
        text = text.lower()

        gene_dict = check_entry(text, gene_dict)

    a_tags = soup.find_all("a")

    for tag in a_tags:
        text = tag.get_text()
        text = text.lower()
        # print(tag)
        gene_dict = check_entry(text, gene_dict)

    vals = gene_dict.values()

    for v in vals:
        if v == 2:
            gene_dict["finished"] = 0
            break
        gene_dict["finished"] = 1
    
    print(gene_dict)
    return gene_dict


def get_entry(infile, outfile, level, col):
    seen = {}

    df = pd.read_csv(infile)
 
    df[f"result"] = df[col].apply(lambda name: find_trait(str(name), check_entry_in_html, seen) or 'Not found')
    dict_cols = pd.json_normalize(df['result'])

    df = pd.concat([df, dict_cols], axis=1)

    df.drop(columns=['result'], inplace=True)

    df.to_csv(outfile, index=False)


if __name__ == "__main__":
    level = "genus"
    get_entry("species_lineage.csv", "ce_genus.csv", level, "Genus")

    # traits = {
    #     'CE_clathrin': 0,
    #     'CE_receptor':1,
    #     'CE_glycoproteins':0,
    #     'other':0,
    #     "finished": 1,
    # }
    # df = pd.read_csv(f"ce_{level}.csv")

    # for k,v in traits.items():
    #     df.loc[df['Genus'].str.contains("Avibirnavirus", na=False), k] = v

    # df.to_csv(f"ce_{level}.csv", index=False)