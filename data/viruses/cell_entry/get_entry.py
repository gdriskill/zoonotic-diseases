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


def ce_missing(infile, target_level):
    df = pd.read_csv(infile)
    df = df[(df['finished'].isna()) | (df['finished'] == 0)]
    df.drop(["CE_clathrin","CE_receptor","CE_glycoproteins","other","finished"], axis=1, inplace=True)
    df.to_csv(f"{target_level}_input.csv", index=False)

def combine_files():
    genus = pd.read_csv("ce_genus.csv")
    family = pd.read_csv("ce_family.csv")

    genus.set_index("Species", inplace=True)
    family.set_index("Species",inplace=True)
    genus.update(family)
    genus.reset_index(inplace=True)

    # traits = ["envelope","circular","double_stranded","rna","segmented","positive_sense","negative_sense", "finished"]
    # for t in traits:
    #     genus[t] = genus[t].where(genus[t].notna(), family[t])
    
    genus.to_csv("ce_total.csv", index=False)

if __name__ == "__main__":
    # level = "family"
    # # get_entry(f"{level}_input.csv", f"ce_{level}.csv", level, "Family")
    # # ce_missing("ce_genus.csv", level)
    # traits = {
    #     'CE_clathrin': 0,
    #     'CE_receptor':1,
    #     'CE_glycoproteins':0,
    #     'other':0,
    #     "finished": 1,
    # }
    # df = pd.read_csv(f"ce_{level}.csv")

    # for k,v in traits.items():
    #     df.loc[df['Order'].str.contains("Reovirales", na=False), k] = v

    # df.to_csv(f"ce_{level}.csv", index=False)

    combine_files()