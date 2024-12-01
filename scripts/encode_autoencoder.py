from AutoEncoder import AutoEncoder
import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

class VirusDataset(Dataset):
    def __init__(self, X, transform=None):
      # self.data = pd.read_csv(csv_path)
      self.transform=transform
      self.X = torch.tensor(X, dtype=torch.float32)  
        
    def __len__(self):
      return len(self.X)  
    
    def __getitem__(self, idx):
      """
      Args:
         idx (int): Index of the data sample.
      """
      row = self.X[idx]
      categorical_features = row[5:]
      other_features = row[1:5]

      if self.transform:
        categorical_features = self.transform
      
      return torch.tensor(categorical_features, dtype=torch.float), torch.tensor(other_features, dtype=torch.long)

class BirdDataset(Dataset):
    def __init__(self, X, transform=None):
      # self.data = pd.read_csv(csv_path)
      self.transform=transform
      self.X = torch.tensor(X, dtype=torch.float32)  
        
    def __len__(self):
      return len(self.X)  
    
    def __getitem__(self, idx):
      """
      Args:
         idx (int): Index of the data sample.
      """
      row = self.X[idx]
      categorical_features = row[7:]
      other_features = row[1:7]

      if self.transform:
        categorical_features = self.transform
      
      return torch.tensor(categorical_features, dtype=torch.float), torch.tensor(other_features, dtype=torch.long)

def encode_data(in_file, out_file, model_file, data_type):
  df = pd.read_csv(in_file)
 
  print(len(df.values[0]))

  if data_type == "bird":
    dataset = BirdDataset(df.values)
    model = AutoEncoder(169)
    not_encoded_columns = ["NCBI Taxon ID","mass","range size","habitat density","migration","evolutionary distinctiveness"]
  else:
    dataset = VirusDataset(df.values)
    model = AutoEncoder(222)
    not_encoded_columns = ["NCBI Taxon ID","size","gc","genes"]

  
  dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

  model.load_state_dict(torch.load(model_file))
  model.eval()

  encoded_data_list = []
  target_list = []

  # Iterate through the DataLoader
  with torch.no_grad(): 
    for batch_idx, (data, target) in enumerate(dataloader):
      # Pass data through the model's encoder
      encoded_data = model.encoder(data)
      
      # Append encoded data and targets to their respective lists
      encoded_data_list.append(encoded_data)
      target_list.append(target)

  # Concatenate all encoded batches and targets into tensors
  encoded_data = torch.cat(encoded_data_list, dim=0)
  target_data = torch.cat(target_list, dim=0)

  # Convert the encoded tensor and target tensor to numpy arrays
  encoded_df = pd.DataFrame(encoded_data.numpy())  # Convert encoded tensor to DataFrame
  target_df = pd.DataFrame(target_data.numpy(), columns=not_encoded_columns)  # Convert multi-target tensor to DataFrame

  # Combine encoded data and multi-target data into a single DataFrame
  final_df = pd.concat([target_df, encoded_df], axis=1)

  # Save the combined data to a CSV file
  final_df.to_csv(out_file, index=False)

def main(bird_file, virus_file, bird_model, virus_model):
  encode_data(bird_file, "./data/hosts/birds/birds_traits_autoencoder.csv", bird_model, "bird")
  encode_data(virus_file, "./data/viruses/virus_traits_autoencoder.csv", virus_model, "virus")


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='autoencoder')

  parser.add_argument('--bird_file', metavar='path', required=True,
                    help='inputfile')

  parser.add_argument('--virus_file', metavar='path', required=True,
                    help='inputfile')
  
  parser.add_argument('--bird_model', metavar='path', required=True,
                    help='inputfile')

  parser.add_argument('--virus_model', metavar='path', required=True,
                    help='inputfile')
                    
  args = parser.parse_args()
  main(args.bird_file, args.virus_file, args.bird_model, args.virus_model)
