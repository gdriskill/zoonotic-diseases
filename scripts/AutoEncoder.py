import torch
import torch.nn as nn
import torch.nn.functional as F

class AutoEncoder(nn.Module):
   # TODO Does this architecture look good? is the use of the relu correct?
   def __init__(self, input_size: int, hidden_size: int=100, latent_size: int=50):
      super(AutoEncoder, self).__init__()

      self.encoder = nn.Sequential(
         nn.Linear(input_size, hidden_size),
         torch.nn.ReLU(),
         nn.Linear(input_size, hidden_size)
      )
     
      self.decoder = nn.Sequential(
         nn.Linear(latent_size, hidden_size),
         torch.nn.ReLU(),
         nn.Linear(latent_size, hidden_size)
      )
     
   def forward(self, x: torch.Tensor):
      encoded = self.encode(x)
      decoded = self.decode(encoded)
      return x
