from sklearn.model_selection import train_test_split
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import torch
import torch.nn as nn
from AutoEncoder import AutoEncoder

class CustomDataset(Dataset):
    def __init__(self, X):

        self.X = torch.tensor(X, dtype=torch.float32)  
        
    def __len__(self):
        return len(self.X)  
    
    def __getitem__(self, idx):
        """
        Args:
            idx (int): Index of the data sample.
        """
        return self.X[idx], self.y[idx]  # Return the feature and the target


def train_model(data: pd.DataFrame, net: AutoEncoder, lr: int, wd: int, epoches: int, quiet=False):
   optimizer = optim.Adagrad(net.parameters(), lr=lr, weight_decay=wd)
   # TODO choose loss
   loss_function = torch.nn.CosineEmbeddingLoss(reduction='none')
   losses = []
   for epoch in range(epoches):
      epoch_loss = 0
      for batch in data:
         net.zero_grad()
         
         output = net(batch)
         
         loss = loss_function(output, batch).sum()
         epoch_loss += loss
         loss.backward()
         optimizer.step()

      avg_loss = epoch_loss / len(data)  
      losses.append(avg_loss)
      if not quiet: print(f"Epoch [{epoch + 1}/{epoches}], Loss: {avg_loss:.4f}")
   
   return net, losses

def test_model(data: pd.DataFrame, net: AutoEncoder):
   net.eval()  
   with torch.no_grad():  
      total_loss = 0
      # TODO choose loss
      loss_function = torch.nn.CosineEmbeddingLoss(reduction='none')

      for batch in data:
         output = net(batch) 
         loss = loss_function(output, batch) 
         total_loss += loss.item()

      avg_loss = total_loss / len(data)

   return avg_loss


# Create train and test DataLoaders
# TODO we dont want to mess with the taxid at all 
# because that is how we id the feature to the nodes in the graph
# So we need to remove that from the data before we encode it 
# and then add it back after?

# TODO probably should make main function and maybe the input file name as an arg
df = pd.read_csv("./data/hosts/birds/birds_traits_processed-onehot.csv")
X_train, X_test = train_test_split(df.values, test_size=0.2, random_state=42)

train_dataset = CustomDataset(X_train)
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = CustomDataset(X_test)
test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)

# Hyperparamters
# TODO hyperparameter tuning
epoches = 250
learning_rate = 1e-3
weighted_decay = 1e-4

# Initialize autoencoder
autoencoder = AutoEncoder(input_size=df.shape[1])

# Train model 
autoencoder, train_losses = train_model(train_dataloader, lr=learning_rate, wd=weighted_decay, epoches=epoches)

# Test the model
test_loss = test_model(test_dataloader, autoencoder)
print(f"Test Loss : {test_loss:.4f}")

# Save the model
torch.save(autoencoder.state_dict(), "autoencoder_model-bird_traits.pth")