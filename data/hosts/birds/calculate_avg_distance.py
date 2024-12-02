import pandas as pd

def calc_avg_distance(host, host_list, distances_df):
    """
    Calculates the average phlyogenetic distance of a given host to a list
    of host.

    Args:
        host_taxid : NCBI Tax ID of the host
        host_list : List of NCBI Tax ID of hosts to calculate distances to.
        distances_df : Dataframe of pairwise phylogenetic distances between
            hosts.
    
    Return:
        float: average distance of this host to the list of hosts
    """
    
    host_distances_df = distances_df.loc[distances_df["Taxid 1"] == host]
    
    
    distance_sum = 0
    count = 0
    for other_host in host_list:
        distance = host_distances_df.loc[host_distances_df["Taxid 2"] == other_host]["Distance"].values
        
        if(len(distance) > 0):
            distance_sum += distance[0]
            count += 1

    try:
        avg_distance = distance_sum/count
    except ZeroDivisionError:
        avg_distance = -1

    return avg_distance

def main(virus_taxid, host_taxid):

    # Dataframe of pairwise phlyogenetic distances between hosts
    distances_df = pd.read_csv("pairwise_distance_avg2.csv")
    # Dataframe of virus-host interactions
    interactions_df = pd.read_csv("filtered_virus_host_interactions.csv")

    # Get list of hosts and non-hosts of the virus
    host_with_virus = interactions_df.loc[interactions_df["Virus Tax ID"] == virus_taxid]["Host Tax ID"].unique()
    host_without_virus =  interactions_df.loc[interactions_df["Virus Tax ID"] != virus_taxid]["Host Tax ID"].unique()
    
    print(len(host_with_virus))
    print(len(host_without_virus))

    # Calculate the average distance of the host to each of the host lists
    avg_distance_virus = calc_avg_distance(host_taxid, host_with_virus, distances_df)
    avg_distance_not_virus = calc_avg_distance(host_taxid, host_without_virus, distances_df)

    print(f"Average distance of host {host_taxid} to hosts of virus {virus_taxid}: {avg_distance_virus}")
    print(f"Average distance of host {host_taxid} to non-hosts of virus {virus_taxid}: {avg_distance_not_virus}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='autoencoder')

    parser.add_argument('--virus_taxid', metavar='path', required=True,
                    help='inputfile')
    
    parser.add_argument('--bird_taxid', metavar='path', required=True,
                        help='inputfile')
                        
    args = parser.parse_args()
    main(int(args.virus_taxid), int(args.bird_taxid))