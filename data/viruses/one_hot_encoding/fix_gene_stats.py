import pandas as pd

df1 = pd.read_csv('gene_stats_oh.csv')

# Load the second CSV (without entry columns)
df2 = pd.read_csv('../species_taxid.csv')

# Merge the two DataFrames on the 'NCBI Taxon ID' column
# Use an 'outer' join to include all rows from both DataFrames
combined_df = pd.merge(df1, df2, on=['Species'], how='outer')
combined_df.drop(columns=["Pathogen Species","Species"], inplace=True)
combined_df = combined_df[combined_df['NCBI Taxon ID'] != "Not found"]

combined_df.to_csv('fixed_gene_stats_oh.csv', index=False)
