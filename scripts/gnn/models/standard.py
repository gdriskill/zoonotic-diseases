from torch_geometric.data import HeteroData
from torch_geometric.nn import SAGEConv, to_hetero
import torch
from torch import Tensor
import torch.nn.functional as F

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels: int):
        super().__init__()

        # NOTE: We're telling SAGEConv to just figure out the input dimension and output size hidden_channels. We could
        # alternatively also have separate linear layers in StandardModel to step this up or down.
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels)
        self.conv3 = SAGEConv(hidden_channels, hidden_channels)
        self.conv4 = SAGEConv(hidden_channels, hidden_channels)
        self.conv5 = SAGEConv(hidden_channels, hidden_channels)
        self.conv6 = SAGEConv(hidden_channels, hidden_channels)
        self.conv7 = SAGEConv(hidden_channels, hidden_channels)
    
    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = F.relu(self.conv3(x, edge_index))
        x = F.relu(self.conv4(x, edge_index))
        x = F.relu(self.conv5(x, edge_index))
        x = F.relu(self.conv6(x, edge_index))
        x = self.conv7(x, edge_index)

        return x
    

class Classifier(torch.nn.Module):
    def forward(self, x_virus: Tensor, x_host: Tensor, edge_label_index: Tensor) -> Tensor:
        edge_feat_virus = x_virus[edge_label_index[0]]
        edge_feat_host = x_host[edge_label_index[1]]

        # We get the dot product for the prediction
        return (edge_feat_virus * edge_feat_host).sum(dim=-1)
    

class StandardModel(torch.nn.Module):
    def __init__(self, hidden_channels, metadata):
        super().__init__()

        self.gnn = GNN(hidden_channels)
        self.gnn = to_hetero(self.gnn, metadata=metadata)
        self.classifier = Classifier()

    def forward(self, data: HeteroData) -> Tensor:
        # The x_dict will just be the node features
        x_dict = {
            'virus': data['virus'].x,
            'host': data['host'].x
        }

        x_dict = self.gnn(x_dict, data.edge_index_dict)
        pred = self.classifier(
            x_dict['virus'],
            x_dict['host'],
            data['virus', 'infects', 'host'].edge_label_index
        )

        return pred

