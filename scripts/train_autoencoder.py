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
      features=row[6:]
      label=row[1]

      if self.transform:
         features = self.transform
      
      return torch.tensor(features, dtype=torch.float), torch.tensor(label, dtype=torch.long)

      #   return self.X[idx], self.y[idx]  # Return the feature and the target


def train_model(dataloader, model: AutoEncoder, lr: int, wd: int, epoches: int, quiet=False):
   optimizer = optim.Adagrad(model.parameters(), lr=lr, weight_decay=wd)

   # TODO choose loss
   loss_function = nn.MSELoss()

   # loss_function = torch.nn.CosineEmbeddingLoss(reduction='none')
   losses = []
   
   for epoch in range(epoches):
      epoch_loss = 0

      for batch, _ in dataloader:
         output = model(batch)
         loss = loss_function(output, batch)
         
         epoch_loss += loss

         optimizer.zero_grad()
         loss.backward()
         optimizer.step()

      # print(batch)

      avg_loss = epoch_loss / len(batch[0])  #number of rows in the tensor
      losses.append(avg_loss)
      if not quiet: print(f"Epoch [{epoch + 1}/{epoches}], Loss: {avg_loss:.4f}")
   
   return model, losses

def test_model(dataloader, model: AutoEncoder):
   model.eval()  
   with torch.no_grad():  
      total_loss = 0
      # TODO choose loss
      # loss_function = torch.nn.CosineEmbeddingLoss(reduction='none')
      loss_function = nn.MSELoss()

      for batch, _ in dataloader:
         output = model(batch) 
         loss = loss_function(output, batch) 
         total_loss += loss.item()

      avg_loss = total_loss / len(batch[0])

   return avg_loss


# Create train and test DataLoaders
# TODO we dont want to mess with the taxid at all 
# because that is how we id the feature to the nodes in the graph
# So we need to remove that from the data before we encode it 
# and then add it back after?

def main(file):
   # df = pd.read_csv("./data/hosts/birds/birds_traits_processed-onehot.csv")
   df = pd.read_csv(file)
   # df.drop(columns="taxid", inplace=True)
   X_train, X_test = train_test_split(df.values, test_size=0.2, random_state=42)

   train_dataset = CustomDataset(X_train)
   train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

   test_dataset = CustomDataset(X_test)
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

   # Train model 
   autoencoder, train_losses = train_model(train_dataloader, autoencoder, lr=learning_rate, wd=weighted_decay, epoches=epoches)

   # Test the model
   test_loss = test_model(test_dataloader, autoencoder)
   print(f"Test Loss : {test_loss:.4f}")

   # Save the model
   torch.save(autoencoder.state_dict(), "autoencoder_model-bird_traits.pth")


#seeing if dataloader works
def test_dataloader(file):
   dataset = CustomDataset(file)
   dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

   for batch_idx, (data, target) in enumerate(dataloader):
      print(batch_idx, data.shape, target.shape)
   

if __name__ == '__main__':
   import argparse

   parser = argparse.ArgumentParser(description='autoencoder')
   parser.add_argument('--file', metavar='path', required=True,
                     help='inputfile')
                     
   args = parser.parse_args()
   main(args.file)







