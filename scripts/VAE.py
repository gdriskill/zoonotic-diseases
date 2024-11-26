import torch
import torch.nn as nn
import torch.nn.functional as F

class VAE(nn.Module):
   def __init__(self, input_size: int, hidden_size: int=100, latent_size: int=50):
      super(VAE, self).__init__()

      self.encoder = nn.Sequential(
         nn.Linear(input_size, hidden_size),
         torch.nn.LeakyReLU(),
         nn.Linear(hidden_size, latent_size)
      )

      self.mean_layer = nn.Linear(latent_size, 2)
      self.logvar_layer = nn.Linear(latent_size, 2)
     
      self.decoder = nn.Sequential(
         nn.Linear(2, latent_size),
         torch.nn.LeakyReLU(),
         nn.Linear(latent_size, hidden_size),
         torch.nn.LeakyReLU(),
         nn.Linear(hidden_size, input_size),
      )
   
   def encode(self, x):
      x = self.encoder(x)
      mean, logvar = self.mean_layer(x), self.logvar_layer(x)
      return mean, logvar

   def decode(self, x):
         return self.decoder(x)

   def reparameterization(self, mean, var):
      device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
      epsilon = torch.randn_like(var).to(device)      
      z = mean + var*epsilon
      return z
     
   def forward(self, x):
      mean, logvar = self.encode(x)
      z = self.reparameterization(mean, logvar)
      x_hat = self.decode(z)
      return x_hat, mean, logvar