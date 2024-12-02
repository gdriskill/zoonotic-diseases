import csv
import pandas as pd
from Bio import Phylo
from multiprocessing import Pool

def calculate_pairwise_distances(tree):
    """
    Calculates the pairwise distance of all the species in a
    single tree.
    """
    pairwise_distances = {}
    for clade1 in tree.get_terminals():
        for clade2 in tree.get_terminals():
            if clade1 != clade2:
                distance = tree.distance(clade1, clade2)
                pairwise_distances[(clade1.name, clade2.name)] = distance
    return pairwise_distances


def process_tree(tree_index, tree):
    """
    Processes a one tree.
    """
    print(f"Processing Tree {tree_index + 1}...")
    distances = calculate_pairwise_distances(tree)
    results = []
    for pair, distance in distances.items():
        results.append([tree_index + 1, pair[0], pair[1], distance])
    print(f"  Tree {tree_index + 1} processed. Calculated {len(distances)} distances.")
    return results

def process_results(file):
    """
    Average the distanes across all trees for each taxon, taxon pair.
    Then adds the NCBI Tax ID for each taxon.

    Args:
        file : filename of a csv file with the columns ['Tree Number', 
            'Taxon 1', 'Taxon 2', 'Distance']
    """
    # Average distances
    distances_df = pd.read_csv("pairwise_distances.csv")
    avg_distance_df = distances_df.groupby(['Taxon 1', 'Taxon 2'])['Distance'].mean().reset_index()

    # Add Tax IDs

    # Open bird traits file to find Tax IDs
    traits_df = pd.read_csv("birds_traits.csv")

    # Add columns for the Tax IDs
    avg_distance_df["Taxid 1"] = 0
    avg_distance_df["Taxid 2"] = 0

    for row in avg_distance_df.iterrows():
        row_idx = row[0]

        # Find the Tax ID for Taxon 1
        taxon1 = row[1]["Taxon 1"]
        taxid1 = traits_df.loc[traits_df["scientific name"] == taxon1]["taxid"].values
        if(len(taxid1) == 0):
            taxid1 = traits_df.loc[traits_df["alternative name"] == taxon1]["taxid"].values

        # Find the Tax ID for Taxon 2
        taxon2 = row[1]["Taxon 2"]
        taxid2 = traits_df.loc[traits_df["scientific name"] == taxon2]["taxid"].values
        if(len(taxid2) == 0):
            taxid2 = traits_df.loc[traits_df["alternative name"] == taxon2]["taxid"].values

        # Save Tax IDs to Dataframe
        avg_distance_df.loc[row_idx, "Taxid 1"] = taxid1
        avg_distance_df.loc[row_idx, "Taxid 2"] = taxid2

    avg_distance_df.to_csv("pairwise_distance_avg.csv")

def main():
    # Open a csv file to save the results
    with open('pairwise_distances.csv', mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Write the header row
        csv_writer.writerow(['Tree Number', 'Taxon 1', 'Taxon 2', 'Distance'])

        # Parse the Nexus file with multiple trees
        with open('output.nex', 'r') as file:
            trees = list(Phylo.parse(file, 'nexus'))
        
        # multiprocessing pool to process trees in parallel
        with Pool() as pool:
            results = pool.starmap(process_tree, [(i, tree) for i, tree in enumerate(trees)])

            # Write all results to CSV after processing
            for tree_results in results:
                for row in tree_results:
                    csv_writer.writerow(row)
    
    print("Pairwise distances saved to 'pairwise_distances.csv'")

if __name__ == "__main__":
    main()

   