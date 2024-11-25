import pandas as pd

name_mappings = {
    "species_lineage.csv": "cleaned/species_lineage.csv",
    "total_genome.csv": "cleaned/genomic_features.csv",
    "final_gene_stats.csv": "cleaned/gene_statistics.csv",
    "with_cyto.csv": "cleaned/cytoplasmic_replication.csv",
    "cr_total.csv": "cleaned/virus_release.csv",
    "ce_total.csv": "cleaned/cell_entry.csv",
}

dataframes = {
    key : pd.read_csv(key) for key in name_mappings.keys()
}

basic_drop_columns = ["Species", "Genus", "Family", "Order", "finished"]

dataframes["ce_total.csv"] = dataframes["ce_total.csv"].drop(columns=basic_drop_columns)
dataframes["ce_total.csv"] = dataframes["ce_total.csv"].rename(columns={"other": "CE_other"})

dataframes["cr_total.csv"] = dataframes["cr_total.csv"].drop(columns=basic_drop_columns)
dataframes["cr_total.csv"] = dataframes["cr_total.csv"].rename(columns={"other": "release_other"})

dataframes["total_genome.csv"] = dataframes["total_genome.csv"].drop(columns=basic_drop_columns)
dataframes["total_genome.csv"] = dataframes["total_genome.csv"].replace([3], [""])

dataframes["final_gene_stats.csv"] = dataframes["final_gene_stats.csv"].drop(columns=["species", "GA_original", "GA"])
dataframes["final_gene_stats.csv"] = pd.merge(dataframes["final_gene_stats.csv"], dataframes["species_lineage.csv"], on=['Species'], how='outer')
dataframes["final_gene_stats.csv"].drop(columns=["Order","Family","Genus","Species", "Unnamed: 0"], inplace=True)

dataframes["with_cyto.csv"] = dataframes["with_cyto.csv"].drop(columns=["Species", "Genus", "Family", "Order"])
dataframes["with_cyto.csv"] = dataframes["with_cyto.csv"].replace([2], [""])

for df in dataframes:
    dataframes[df] = dataframes[df][dataframes[df]['NCBI Taxon ID'] != "Not found"]
    dataframes[df]= dataframes[df].drop_duplicates(subset=['NCBI Taxon ID'])
    dataframes[df].to_csv(name_mappings[df], index=False)
