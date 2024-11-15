from scrape import *

ssrnaneg = ["ssrna(-)", "negative-stranded rna", "ssrna-"]
ssrnapos = ["ssrna(+)", "positive-stranded rna", "ssrna+"]


def check_ss_rna(text, gene_dict):
    for w in ssrnapos:
        if w in text:
            #print("positive")
            gene_dict["positive_sense"] = 1
            gene_dict["negative_sense"] = 0
            gene_dict["double_stranded"] = 0
            gene_dict["rna"] = 1

    for w in ssrnaneg:
        if w in text:
            #print("negative")
            gene_dict["positive_sense"] = 0
            gene_dict["negative_sense"] = 1
            gene_dict["double_stranded"] = 0
            gene_dict["rna"] = 1

    if "ssdna(+)" in text:
        #print("positive")
        gene_dict["positive_sense"] = 1
        gene_dict["negative_sense"] = 0
        gene_dict["double_stranded"] = 0
        gene_dict["rna"] = 0
    if "ssdna(-)" in text:
        #print("negative")
        gene_dict["positive_sense"] = 0
        gene_dict["negative_sense"] = 1
        gene_dict["double_stranded"] = 0
        gene_dict["rna"] = 0
    
    if "ssdna " in text:
        gene_dict["double_stranded"] = 0
        gene_dict["rna"] = 0
        gene_dict["positive_sense"] = 0
        gene_dict["negative_sense"] = 0
    
    # if "there are coding regions in both the virion (positive) and complementary (negative) sense strands" in text:
    #     gene_dict["positive_sense"] = 1
    #     gene_dict["negative_sense"] = 1
    
    if "dsdna" in text or "double-stranded dna" in text:
        #print("here4")

        gene_dict["positive_sense"] = 0
        gene_dict["negative_sense"] = 0
        gene_dict["double_stranded"] = 1
        gene_dict["rna"] = 0
    if "dsrna" in text or "double-stranded rna" in text:
        #print("here")
        gene_dict["positive_sense"] = 0
        gene_dict["negative_sense"] = 0
        gene_dict["double_stranded"] = 1
        gene_dict["rna"] = 1
    
    return gene_dict

def check_gene_struct(soup):
    ps = soup.find_all("p")

    gene_dict = {
        'envelope': 2,
        'circular':2,
        'double_stranded':2,
        'rna':2,
        'segmented':2,
        "positive_sense": 2,
        "negative_sense": 2,
        "finished": 0,
    }

    non_env_list = ["non-enveloped", "Non-enveloped", "non enveloped", "Non enveloped"]


    for p in ps:
        text = p.get_text()
        text = text.lower()
        # print(text)
        for w in non_env_list:
            if w in text:
                gene_dict["envelope"] = 0
        
        if gene_dict["envelope"] == 2 and "enveloped" in text:
        #print("env")
            gene_dict["envelope"] = 1

        if "segmented" in text:
            #print("yes seg")
            gene_dict["segmented"] = 1

        if "monopartite" in text:
            #print("no seg")
            gene_dict["segmented"] = 0

        if "linear" in text:
            #print("no circular")
            gene_dict["circular"] = 0
        if "circular" in text:
            #print("yes circular")
            gene_dict["circular"] = 1
        
        gene_dict = check_ss_rna(text, gene_dict)
        
    if gene_dict["envelope"] == 2:
        #print("env")
        gene_dict["envelope"] = 3
    
    if gene_dict["segmented"] == 2:
        gene_dict["segmented"] = 3

    a_tags = soup.find_all("a")

    for tag in a_tags:
        text = tag.get_text()
        text = text.lower()

        gene_dict = check_ss_rna(text, gene_dict)
    
    vals = gene_dict.values()
    for v in vals:
        if v == 2:
            gene_dict["finished"] = 0
            break
        gene_dict["finished"] = 1
    
    print(vals)

    return gene_dict

def get_genome(infile, outfile, level, col):
    seen = {}

    df = pd.read_csv(infile)
 
    df[f"result"] = df[col].apply(lambda name: find_trait(str(name), check_gene_struct, seen) or 'Not found')
    dict_cols = pd.json_normalize(df['result'])

    df = pd.concat([df, dict_cols], axis=1)

    df.drop(columns=['result'], inplace=True)

    df.to_csv(outfile, index=False)

def fix_genome(infile, outfile, level, col):
    seen = {}

    df = pd.read_csv(infile)
 
    df.update(df[col].apply(lambda name: find_trait(str(name), check_gene_struct, seen) or 'Not found').apply(pd.Series))
    # dict_cols = pd.json_normalize(df['result'])

    # df = pd.concat([df, dict_cols], axis=1)

    # df.drop(columns=['result'], inplace=True)

    df.to_csv(outfile, index=False)

def make_missing_file(infile, target_level):
    df = pd.read_csv(infile)
    df = df[(df['finished'].isna()) | (df['finished'] == 0)]
    df.drop(["envelope","circular","double_stranded","rna","segmented","positive_sense","negative_sense","finished"], axis=1, inplace=True)
    df.to_csv(f"{target_level}_input.csv", index=False)

def combine_files():
    genus = pd.read_csv("total_genome.csv")
    family = pd.read_csv("genome_order_temp.csv")

    genus.set_index("Species", inplace=True)
    family.set_index("Species",inplace=True)
    genus.update(family)
    genus.reset_index(inplace=True)

    # traits = ["envelope","circular","double_stranded","rna","segmented","positive_sense","negative_sense", "finished"]
    # for t in traits:
    #     genus[t] = genus[t].where(genus[t].notna(), family[t])
    
    genus.to_csv("total_genome.csv", index=False)

if __name__ == "__main__":
    combine_files()
    # level = "order"
    # make_missing_file("genome_genus.csv", level)
    # get_genome(f"temp.csv", f"genome_{level}_temp.csv", level, "Genus")
    # fix_genome(f"genome_{level}.csv", f"genome_{level}_temp.csv", level, "Order")
    # combine_files()
    # df = pd.read_csv("genome_struct/total_genome.csv")
    # df = df[df["finished"] == 0]
    # df.to_csv("unfinished_genome.csv", index=False)
    # traits = {
    #     "envelope": 3.0,
    #     "circular": 1.0,
    #     "double_stranded": 0.0,
    #     "rna": 0.0,
    #     "segmented":3.0, 
    #     "positive_sense": 0.0,
    #     "negative_sense": 0.0,
    #     "finished":1.0
    # }
    # df = pd.read_csv(f"genome_{level}_temp.csv")

    # for k,v in traits.items():
    #     df.loc[df['Species'].str.contains("CRESS-DNA-virus sp.", na=False), k] = v

    # df.to_csv(f"genome_{level}_temp.csv", index=False)
    # combine_files()