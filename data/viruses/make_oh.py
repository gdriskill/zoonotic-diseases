import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def cyto_oh():

    # Read the original CSV
    df = pd.read_csv('with_cyto.csv')

    df['cytoplasm'] = (df['cytoplasm'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    # df['cytoplasm_no'] = (df['cytoplasm'] == 0).astype(int)   # 1 for 'no', 0 otherwise
    df['cytoplasm_na'] = (df['cytoplasm'] == 2).astype(int)   # 1 for 'unknown', 0 otherwise

    # Drop the original cytoplasm column
    # df = df.drop(columns=['cytoplasm'])
    df = df.drop(columns=['Species', 'Order', 'Family', 'Genus'])
    df = df[df['NCBI Taxon ID'] != "Not found"]

    # Save the new DataFrame to a new CSV
    df.to_csv('one_hot_encoding/cyto_oh.csv', index=False)


def genome_oh():

    # Read the original CSV
    df = pd.read_csv('total_genome.csv')

    df['envelope'] = (df['envelope'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    # df['envelope_no'] = (df['envelope'] == 0).astype(int)   # 1 for 'no', 0 otherwise
    df['envelope_na'] = (df['envelope'] == 3).astype(int)   # 1 for 'unknown', 0 otherwise

    # df = df.drop(columns=['envelope'])

    df['circular'] = (df['circular'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    # df['circular_no'] = (df['circular'] == 0).astype(int)   # 1 for 'no', 0 otherwise
    df['circular_na'] = df['circular'].isnull().astype(int)   # 1 for 'no', 0 otherwise


    # df = df.drop(columns=['circular'])

    df['double_stranded'] = (df['double_stranded'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['double_stranded_na'] = df['double_stranded'].isnull().astype(int)   # 1 for 'no', 0 otherwise


    df['rna'] = (df['rna'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['rna_na'] = df['rna'].isnull().astype(int)    # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['rna'])

    
    df['segmented'] = (df['segmented'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    # df['segmented_no'] = (df['segmented'] == 0).astype(int)   # 1 for 'no', 0 otherwise
    df['segmented_na'] = (df['segmented'] == 3).astype(int)   # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['segmented'])

    df['positive_sense'] = (df['positive_sense'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['positive_na'] = df['positive_sense'].isnull().astype(int)    # 1 for 'no', 0 otherwise
    
    df['negative_sense'] = (df['negative_sense'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['negative_na'] = df['negative_sense'].isnull().astype(int)   # 1 for 'no', 0 otherwise

    cond = df['double_stranded'] == True
    df.loc[cond, ['positive_sense', 'negative_sense']] = 0

    # df = df.drop(columns=['double_stranded'])
    # df = df.drop(columns=['positive_sense'])
    # df = df.drop(columns=['negative_sense'])
    df = df.drop(columns=['finished'])
    df = df.drop(columns=['Species', 'Order', 'Family', 'Genus'])
    df = df[df['NCBI Taxon ID'] != "Not found"]

    # Save the new DataFrame to a new CSV
    df.to_csv('one_hot_encoding/genomic_struct.csv', index=False)

def cr_oh():
    df = pd.read_csv('cr_total.csv')

    df['budding'] = (df['budding'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['budding_na'] = df['budding'].isnull().astype(int)   # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['budding'])

    df['lysis'] = (df['lysis'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['lysis_na'] = df['lysis'].isnull().astype(int)  # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['lysis'])

    df['other_release'] = (df['other'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['other_release_na'] = df['other'].isnull().astype(int)  # 1 for 'no', 0 otherwise
    df = df.drop(columns=['other'])
    df = df.drop(columns=['finished'])
    df = df.drop(columns=['Species', 'Order', 'Family', 'Genus'])
    df = df[df['NCBI Taxon ID'] != "Not found"]

    df.to_csv('one_hot_encoding/cr_oh.csv', index=False)


def ce_oh():
    df = pd.read_csv('cell_entry/ce_total.csv')

    df['CE_clathrin'] = (df['CE_clathrin'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['CE_clathrin_na'] = df['CE_clathrin'].isnull().astype(int)  # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['CE_clathrin'])

    df['CE_receptor'] = (df['CE_receptor'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['CE_receptor_na'] = df['CE_receptor'].isnull().astype(int)  # 1 for 'no', 0 otherwise

    # df = df.drop(columns=['CE_receptor'])

    df['CE_glycoproteins'] = (df['CE_glycoproteins'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['CE_glycoproteins_na'] = df['CE_glycoproteins'].isnull().astype(int)   # 1 for 'no', 0 otherwise
    
    # df = df.drop(columns=['CE_glycoproteins'])

    df['other_entry'] = (df['other'] == 1).astype(int)  # 1 for 'yes', 0 otherwise
    df['other_entry_na'] = df['other'].isnull().astype(int)
    df = df[df['NCBI Taxon ID'] != "Not found"]


    df = df.drop(columns=['other'])
    df = df.drop(columns=['finished'])
    df = df.drop(columns=['Species', 'Order', 'Family', 'Genus'])



    df.to_csv('one_hot_encoding/ce_oh.csv', index=False)

def gene_stats_oh():
    df = pd.read_csv('final_gene_stats.csv')

    df['GA_missing'] = df['GA'].isnull().astype(int) | (df['GA'] == 0).astype(int)
    # df = df.drop(columns=['GA'])

    df['size_missing'] = df['size'].isnull().astype(int)
    # df = df.drop(columns=['size'])

    df['gc_missing'] = df['gc'].isnull().astype(int)
    # df = df.drop(columns=['gc'])

    df['genes_missing'] = df['genes'].isnull().astype(int)

    df = df.drop(columns=['GA_original'])
    df = df.drop(columns=['Species', 'Order', 'Family', 'Genus'])
    df = df[df['NCBI Taxon ID'] != "Not found"]


    df.to_csv('one_hot_encoding/gene_stats_oh.csv', index=False)

def lineage_oh():
    df = pd.read_csv('species_lineage.csv')

    categorical_cols = ["Order","Family","Genus"]

    encoder = OneHotEncoder(sparse_output=False)

    one_hot_encoded = encoder.fit_transform(df[categorical_cols])
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_cols))
    
    processed_df = pd.concat([df, one_hot_encoded_df], axis=1)

    # drop the unencoded categorical columns
    processed_df = processed_df.drop(categorical_cols, axis=1)

    processed_df = processed_df.drop(columns=['Species'])
    processed_df = processed_df[processed_df['NCBI Taxon ID'] != "Not found"]

    # Save the processed dataframe
    processed_df.to_csv("one_hot_encoding/lineage_oh.csv", index=False)

if __name__ == "__main__":
    cyto_oh()
    genome_oh()
    cr_oh()
    ce_oh()
    lineage_oh()