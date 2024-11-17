import pandas as pd
from scrape import *


def check_entry(text, gene_dict):
    # print(text)
    if "lysis" in text:
        gene_dict['budding']= 0
        gene_dict['lysis']= 1
        gene_dict['other']= 0
    
    if "budding" in text or "bud " in text or "buds " in text:
        gene_dict['budding']= 1
        gene_dict['lysis']= 0
        gene_dict['other']= 0
    
    return gene_dict
    

def check_release_in_html(soup):
    ps = soup.find_all("p")

    gene_dict = {
        'budding': 2,
        'lysis':2,
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
        gene_dict = check_entry(text, gene_dict)

    vals = gene_dict.values()

    for v in vals:
        if v == 2:
            gene_dict["finished"] = 0
            break
        gene_dict["finished"] = 1
    
    print(gene_dict)
    return gene_dict


def get_release(infile, outfile, level, col):
    seen = {}

    df = pd.read_csv(infile)
 
    df[f"result"] = df[col].apply(lambda name: find_trait(str(name), check_release_in_html, seen) or 'Not found')
    dict_cols = pd.json_normalize(df['result'])

    df = pd.concat([df, dict_cols], axis=1)

    df.drop(columns=['result'], inplace=True)

    df.to_csv(outfile, index=False)


def cr_missing(infile, target_level):
    df = pd.read_csv(infile)
    df = df[(df['finished'].isna()) | (df['finished'] == 0)]
    df.drop(["budding","lysis","other","finished"], axis=1, inplace=True)
    df.to_csv(f"{target_level}_input.csv", index=False)

def combine_files():
    genus = pd.read_csv("cr_genus.csv")
    family = pd.read_csv("cr_family.csv")

    genus.set_index("Species", inplace=True)
    family.set_index("Species",inplace=True)
    genus.update(family)
    genus.reset_index(inplace=True)

    # traits = ["envelope","circular","double_stranded","rna","segmented","positive_sense","negative_sense", "finished"]
    # for t in traits:
    #     genus[t] = genus[t].where(genus[t].notna(), family[t])
    
    genus.to_csv("cr_total.csv", index=False)

if __name__ == "__main__":
    # level = "family"
    # # get_release(f"{level}_input.csv", f"cr_{level}.csv", level, "Family")
    # # cr_missing("cr_genus.csv", level)
    # traits = {
    #     'budding': 0,
    #     'lysis':1,
    #     'other':0,
    #     "finished": 1,
    # }
    # df = pd.read_csv(f"cr_{level}.csv")

    # for k,v in traits.items():
    #     df.loc[df['Order'].str.contains("Picornavirales", na=False), k] = v

    # df.to_csv(f"cr_{level}.csv", index=False)

    combine_files()