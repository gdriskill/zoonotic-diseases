import pandas as pd

df1 = pd.read_csv("species_lineage.csv")
df2 = pd.read_csv("genomic_features.csv")
df3 = pd.read_csv("gene_statistics.csv")
df4 = pd.read_csv("virus_release.csv")
df5 = pd.read_csv("cytoplasmic_replication.csv")
df6 = pd.read_csv("cell_entry.csv")

frames = [df1, df2, df3, df4, df5, df6]

for i in range(len(frames)):
    frames[i]["NCBI Taxon ID"] = frames[i]["NCBI Taxon ID"].astype(int)
 
df1, df2, df3, df4, df5, df6 = frames

combined_df = pd.merge(df1, df2, on=['NCBI Taxon ID'], how='inner')
combined_df = pd.merge(combined_df, df3, on=['NCBI Taxon ID'], how='outer')
combined_df = pd.merge(combined_df, df4, on=['NCBI Taxon ID'], how='outer')

combined_df = pd.merge(combined_df, df5, on=['NCBI Taxon ID'], how='outer')
combined_df = pd.merge(combined_df, df6, on=['NCBI Taxon ID'], how='outer')

# Save the combined DataFrame to a new CSV
combined_df.to_csv('virus_traits_all_viruses.csv', index=False)

combined_df.dropna(subset=[
    "Order", "Family","Genus","envelope","circular",
    "double_stranded","rna","segmented","positive_sense",
    "negative_sense","size","gc","genes","budding","lysis",
    "release_other","cytoplasm","CE_clathrin","CE_receptor",
    "CE_glycoproteins","CE_other"], how="all", inplace=True)

combined_df.to_csv('virus_traits.csv', index=False)
