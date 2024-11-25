import pandas as pd

df1 = pd.read_csv('lineage_oh.csv')

# Load the second CSV (without entry columns)
df2 = pd.read_csv('genomic_struct.csv')

df3 = pd.read_csv('fixed_gene_stats_oh.csv')
df4 = pd.read_csv('cyto_oh.csv')
df5 = pd.read_csv('cr_oh.csv')
df6 = pd.read_csv('ce_oh.csv')

frames = [df1, df2, df3, df4, df5, df6]

for i in range(len(frames)):
    frames[i] = frames[i].drop_duplicates(subset=['NCBI Taxon ID'])
    frames[i]["NCBI Taxon ID"] = frames[i]["NCBI Taxon ID"].astype(int)
 
df1, df2, df3, df4, df5, df6 = frames

# Merge the two DataFrames on the 'NCBI Taxon ID' column
# Use an 'outer' join to include all rows from both DataFrames
# print(df1['NCBI Taxon ID'].value_counts())
# print(df2['NCBI Taxon ID'].value_counts())
combined_df = pd.merge(df1, df2, on=['NCBI Taxon ID'], how='inner')
combined_df = pd.merge(combined_df, df3, on=['NCBI Taxon ID'], how='outer')
combined_df = pd.merge(combined_df, df4, on=['NCBI Taxon ID'], how='outer')

combined_df = pd.merge(combined_df, df5, on=['NCBI Taxon ID'], how='outer')
combined_df = pd.merge(combined_df, df6, on=['NCBI Taxon ID'], how='outer')

# Save the combined DataFrame to a new CSV
combined_df.to_csv('combined_output.csv', index=False)

print("Rows combined and saved to 'combined_output.csv'.")