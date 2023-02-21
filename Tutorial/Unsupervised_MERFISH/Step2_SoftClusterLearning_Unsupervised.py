import torch
import torch.nn.functional as F
from torch.nn import Linear
from torch_geometric.loader import DenseDataLoader
from torch_geometric.nn import DenseGraphConv, dense_mincut_pool
from torch_geometric.data import InMemoryDataset
import torch_geometric.transforms as T

import os
import numpy
import datetime
import csv
import shutil


# Hyperparameters
max_nodes = 6000   #This number must be higher than the largest number of cells in each image in the studied dataset.
Num_Run = 20
Num_Epoch = 3000
Num_TCN = 9
Num_Dimension = 128
LearningRate = 0.0001

## Load dataset from constructed Dataset.
class SpatialOmicsImageDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(SpatialOmicsImageDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return ['SpatialOmicsImageDataset.pt']

    def download(self):
        pass
    
    def process(self):
        # Read data_list into huge `Data` list.
        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])

dataset = SpatialOmicsImageDataset('./', transform=T.ToDense(max_nodes))


class Net(torch.nn.Module):
    def __init__(self, in_channels, out_channels, hidden_channels=Num_Dimension):
        super(Net, self).__init__()

        self.conv1 = DenseGraphConv(in_channels, hidden_channels)
        num_cluster1 = Num_TCN   #This is a hyperparameter.
        self.pool1 = Linear(hidden_channels, num_cluster1)

    def forward(self, x, adj, mask=None):

        x = F.relu(self.conv1(x, adj, mask))
        s = self.pool1(x)  #Here "s" is a non-softmax tensor.
        x, adj, mc1, o1 = dense_mincut_pool(x, adj, s, mask)
        #Save important clustering results_1.
        ClusterAssignTensor_1 = s
        ClusterAdjTensor_1 = adj

        return F.log_softmax(x, dim=-1), mc1, o1, ClusterAssignTensor_1, ClusterAdjTensor_1


def train(epoch):
    model.train()
    loss_all = 0

    for data in train_loader:
        data = data.to(device)
        optimizer.zero_grad()
        out, mc_loss, o_loss, _, _ = model(data.x, data.adj, data.mask)
        loss = mc_loss + o_loss
        loss.backward()
        loss_all += loss.item()
        optimizer.step()
    return loss_all


normal_index = [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]  #Image index for AnimalID=1. (Example female in the original data paper.)
train_index = normal_index[2:3]  #Extract a single graph.

train_dataset = dataset[train_index]
train_loader = DenseDataLoader(train_dataset, batch_size=1)
all_sample_loader = DenseDataLoader(train_dataset, batch_size=1)

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
run_number = 1
while run_number <= Num_Run:  #Generate multiple independent runs for soft consensus clustering.

    print(f"This is Run{run_number:02d}")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Net(dataset.num_features, dataset.num_classes).to(device)  #Initializing the model.
    optimizer = torch.optim.Adam(model.parameters(), lr=LearningRate)
    
    RunFolderName = "Run" + str(run_number)
    os.makedirs(RunFolderName)  #Creating the Run folder.
    filename_0 = RunFolderName + "/Epoch_TrainLoss.csv"
    headers_0 = ["Epoch", "TrainLoss"]
    with open(filename_0, "w", newline='') as f0:
        f0_csv = csv.writer(f0)
        f0_csv.writerow(headers_0)

    previous_loss = float("inf")  #Initialization.
    for epoch in range(1, Num_Epoch+1):  #Specify the number of epoch in each independent run.
        train_loss = train(epoch)

        #print(f"Epoch: {epoch:03d}, Train Loss: {train_loss:.4f}")
        with open(filename_0, "a", newline='') as f0:
            f0_csv = csv.writer(f0)
            f0_csv.writerow([epoch, train_loss])
        
        if train_loss == 0 and train_loss == previous_loss:  #If two consecutive losses are both zeros, training gets stuck.
            break  #stop the training.
        else:
            previous_loss = train_loss

    print(f"Final train loss is {train_loss:.4f}")
    if train_loss >= -0.6:   #This is an empirical cutoff for final train loss.
        shutil.rmtree(RunFolderName)  #Remove the specific folder and all files below it for re-creating the Run folder.
        continue  #restart this run.

    #Extract the soft clustering matrix using the trained model.
    for EachData in all_sample_loader:
        EachData = EachData.to(device)
        TestModelResult = model(EachData.x, EachData.adj, EachData.mask)

        ClusterAssignMatrix1 = TestModelResult[3][0, :, :]
        ClusterAssignMatrix1 = torch.softmax(ClusterAssignMatrix1, dim=-1)  #Checked, consistent with function built in "dense_mincut_pool".
        ClusterAssignMatrix1 = ClusterAssignMatrix1.detach().numpy()
        filename1 = RunFolderName + "/ClusterAssignMatrix1.csv"
        numpy.savetxt(filename1, ClusterAssignMatrix1, delimiter=',')

        ClusterAdjMatrix1 = TestModelResult[4][0, :, :]
        ClusterAdjMatrix1 = ClusterAdjMatrix1.detach().numpy()
        filename2 = RunFolderName + "/ClusterAdjMatrix1.csv"
        numpy.savetxt(filename2, ClusterAdjMatrix1, delimiter=',')

        NodeMask = EachData.mask
        NodeMask = numpy.array(NodeMask)
        filename3 = RunFolderName + "/NodeMask.csv"
        numpy.savetxt(filename3, NodeMask.T, delimiter=',', fmt='%i')  #save as integers.

        GraphIdxArray = numpy.array(EachData.graph_idx.view(-1))
        filename4 = RunFolderName + "/GraphIdx.csv"
        numpy.savetxt(filename4, GraphIdxArray, delimiter=',', fmt='%i')  #save as integer.

    run_number = run_number + 1

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


