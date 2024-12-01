from sklearn.model_selection import train_test_split
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import torch
import torch.nn as nn
from AutoEncoder import AutoEncoder

#TODO normalize continuous features?

class CustomDataset(Dataset):
    def __init__(self, X, transform=None):
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
      features=row[7:]
      label=row[1]

      if self.transform:
         features = self.transform
      
      return torch.tensor(features, dtype=torch.float), torch.tensor(label, dtype=torch.long)

      #   return self.X[idx], self.y[idx]  # Return the feature and the target


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



def train_model(dataloader, model: AutoEncoder, lr: int, wd: int, epoches: int, quiet=False):
   optimizer = optim.Adagrad(model.parameters(), lr=lr, weight_decay=wd)

   # TODO choose loss
   #loss_function = nn.MSELoss()

   loss_function = torch.nn.CosineEmbeddingLoss(reduction='mean')
   losses = []
   
   for epoch in range(epoches):
      epoch_loss = 0

      for batch, _ in dataloader:
         output = model(batch)
         target = torch.ones(output.size(0))
         loss = loss_function(output, batch, target)

         epoch_loss += loss

         optimizer.zero_grad()
         loss.backward()
         optimizer.step()

      avg_loss = epoch_loss / len(batch[0])  #number of rows in the tensor
      losses.append(avg_loss)
      if not quiet: print(f"Epoch [{epoch + 1}/{epoches}], Loss: {avg_loss:.4f}")
   
   return model, losses

def test_model(dataloader, model: AutoEncoder):
   model.eval()  
   with torch.no_grad():  
      total_loss = 0
      # TODO choose loss
      loss_function = torch.nn.CosineEmbeddingLoss(reduction='mean')
      #loss_function = nn.MSELoss()

      for batch, _ in dataloader:
         output = model(batch) 
         target = torch.ones(output.size(0))
         loss = loss_function(output, batch, target) 
         total_loss += loss.item()

      avg_loss = total_loss / len(batch[0])

   return avg_loss

def create_autoencoder(in_file, out_file, data_type):
   # df = pd.read_csv("./data/hosts/birds/birds_traits_processed-onehot.csv")
   df = pd.read_csv(in_file)
   # df.drop(columns="taxid", inplace=True)
   X_train, X_test = train_test_split(df.values, test_size=0.2, random_state=42)

   if data_type == "bird":
      train_dataset = BirdDataset(X_train)
      test_dataset = BirdDataset(X_test)
   else:
      train_dataset = VirusDataset(X_train)
      test_dataset = VirusDataset(X_test)

   train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
   test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)

   # Hyperparamters
   # TODO hyperparameter tuning
   epoches = 250
   learning_rate = 1e-3
   weighted_decay = 1e-6

   # Initialize autoencoder
   # print("**********************")
   # print()

   autoencoder = AutoEncoder(input_size=train_dataset.__getitem__(0)[0].size(0))
   print(train_dataset.__getitem__(0)[0].size(0))
   # Train model 
   autoencoder, train_losses = train_model(train_dataloader, autoencoder, lr=learning_rate, wd=weighted_decay, epoches=epoches, quiet=True)

   # Test the model
   test_loss = test_model(test_dataloader, autoencoder)
   print(f"Test Loss : {test_loss:.4f}")

   # Save the model
   torch.save(autoencoder.state_dict(), out_file)

# Create train and test DataLoaders
# TODO we dont want to mess with the taxid at all 
# because that is how we id the feature to the nodes in the graph
# So we need to remove that from the data before we encode it 
# and then add it back after?

def main(bird_file, virus_file):
  create_autoencoder(bird_file, "./models/autoencoder_model-bird_traits.pth", "bird")
  create_autoencoder(virus_file, "./models/autoencoder_model-virus_traits.pth", "virus")


#seeing if dataloader works
def test_dataloader(file):
   dataset = CustomDataset(file)
   dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

   for batch_idx, (data, target) in enumerate(dataloader):
      print(batch_idx, data.shape, target.shape)
   

if __name__ == '__main__':
   import argparse

   parser = argparse.ArgumentParser(description='autoencoder')
   parser.add_argument('--bird_file', metavar='path', required=True,
                     help='inputfile')

   parser.add_argument('--virus_file', metavar='path', required=True,
                     help='inputfile')
                     
   args = parser.parse_args()
   main(args.bird_file, args.virus_file)







