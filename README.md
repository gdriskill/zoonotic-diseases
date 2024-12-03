# Predicting Missing Virus-Host Links for Avian Hosts using Graph Neural Networks
Fall 2024 CSE 8803 EPI project

## Overview
This project aims to apply GNNs to analyze host-pathogen and interspecies avian datasets and predict unknown associations between birds and viruses. This will grant better insight into a virus’s range of hosts and by extension their potential to spill over to humans. The data folder contains the datasets needed to run the model. The scripts folder contains the code to train and test the GNNs model.

## Installation Instructions
To set up the necessary environment, create a Conda environment using the environment.yaml file.

```conda env create -f environment.yaml```

Next, activate the newly created environment.

```conda activate avian_zoonosis```

## Usage
To train and evaluate the model on the mammalian dataset used in Wardeh et al, run the code in `scripts/gnn/train_eval-dfencoder.ipynb`.\
A cleaned version of the Wardeh et al. dataset is found in `data/divide_and_conquer`.

To train and evaluate the model on the avian dataset we created, run the code in scripts/gnn/train_eval_avian-dfencoder.ipynb. This will also ouput the top most likely predicted previously unobserved interactions.\
The dataset for avian-virus interactions is found under `data/interactions/NCBI`.\
The dataset for avian traits is found under `data/hosts/birds`.\
The dataset for virus traits is found under `data/viruses`.

To analyze predicted interactions by calculating the average distance of a host to the known hosts of a virus and the average distance of a host to the rest of the avian species, run data/hosts/bird/calculate_avg_distance.py:

``python .\calculate_avg_distance.py --virus_taxid <virus taxid> --bird_taxid <avian host taxid>``

The folder `scripts` contains scripts used for this project. \
The notebook `scripts/gnn/train_eval.ipynb` runs the GNN on the mammalian dataset without dfencoder.\
The notebook `scripts/gnn/train_eval-dfencoder.ipynb` runs the GNN on the mammalian dataset with dfencoder.\
The notebook `scripts/gnn/train_eval_avian-dfencoder.ipynb` runs the GNN on the avian dataset with dfencoder.\
The folder `scripts/graphs` contains graphs output by `scripts/gnn/train_eval_avian-dfencoder.ipynb` and `scripts/gnn/train_eval-dfencoder.ipynb`. \
The file `scripts/graphs/models/standard.py` contains the implementation of the GNN.  \

We also wrote our own autoencoders that were not used for the final results. Code is in `scripts/AutoEncoder.py`, `scripts/encode_autoencoder.py`, and `scripts/train_autoencoder.py`. These models are saved under `models`.

