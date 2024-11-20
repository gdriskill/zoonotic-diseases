import csv
import time
from Bio import Phylo
from multiprocessing import Pool

# Function to calculate pairwise distances for a single tree
def calculate_pairwise_distances(tree):
    pairwise_distances = {}
    for clade1 in tree.get_terminals():
        for clade2 in tree.get_terminals():
            if clade1 != clade2:
                distance = tree.distance(clade1, clade2)
                pairwise_distances[(clade1.name, clade2.name)] = distance
    return pairwise_distances

# Function to process one tree and save distances to CSV
def process_tree(tree_index, tree):
    print(f"Processing Tree {tree_index + 1}...")
    distances = calculate_pairwise_distances(tree)
    results = []
    for pair, distance in distances.items():
        results.append([tree_index + 1, pair[0], pair[1], distance])
    print(f"  Tree {tree_index + 1} processed. Calculated {len(distances)} distances.")
    return results

def main():
    # Open the CSV file to save the distances
    with open('pairwise_distances.csv', mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Write the header row
        csv_writer.writerow(['Tree Number', 'Taxon 1', 'Taxon 2', 'Distance'])

        # Parse the Nexus file with multiple trees
        with open('output2.nex', 'r') as file:
            trees = list(Phylo.parse(file, 'nexus'))
        
        # Start the multiprocessing pool
        with Pool() as pool:
            # Process each tree in parallel
            results = pool.starmap(process_tree, [(i, tree) for i, tree in enumerate(trees)])

            # Write all results to CSV after processing
            for tree_results in results:
                for row in tree_results:
                    csv_writer.writerow(row)
    
    print("Pairwise distances saved to 'pairwise_distances.csv'")

if __name__ == "__main__":
    # Start measuring time
    start_time = time.time()

    # Run the main function
    main()

    # End measuring time
    end_time = time.time()

    # Print total execution time
    print(f"Total execution time: {end_time - start_time} seconds")
