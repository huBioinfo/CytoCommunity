from sklearn.neighbors import kneighbors_graph
import numpy as np
import pandas as pd
import math
import datetime
import os
import torch
import torch_geometric.transforms as T
from torch_geometric.data import Data, InMemoryDataset


## Hyperparameters
InputFolderName = "./MERFISH-Brain_Input/"
KNN_K = 69


## Import image name list.
Region_filename = InputFolderName + "ImageNameList.txt"
region_name_list = pd.read_csv(
        Region_filename,
        sep="\t",  # tab-separated
        header=None,  # no heading row
        names=["Image"],  # set our own names for the columns
    )


## Below is for generation of topology structures (edges) of cellular spatial graphs.
ThisStep_OutputFolderName = "./Step1_Output/"
os.makedirs(ThisStep_OutputFolderName)
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("Constructing topology structures of KNN graphs...")
for graph_index in range(0, len(region_name_list)):

    print(f"This is image-{graph_index}")
    # Import target graph x/y coordinates.
    region_name = region_name_list.Image[graph_index]
    GraphCoord_filename = InputFolderName + region_name + "_Coordinates.txt"
    x_y_coordinates = np.loadtxt(GraphCoord_filename, dtype='float', delimiter="\t")

    K = KNN_K
    KNNgraph_sparse = kneighbors_graph(x_y_coordinates, K, mode='connectivity', include_self=False, n_jobs=-1)  #should NOT include itself as a nearest neighbor. Checked. "-1" means using all available cores.
    KNNgraph_AdjMat = KNNgraph_sparse.toarray()
    # Make the graph to undirected.
    KNNgraph_AdjMat_fix = KNNgraph_AdjMat + KNNgraph_AdjMat.T  #2min and cost one hundred memory.
    # Extract and write the edge index of the undirected graph.
    KNNgraph_EdgeIndex = np.argwhere(KNNgraph_AdjMat_fix > 0)  #1min
    filename0 = ThisStep_OutputFolderName + region_name + "_EdgeIndex.txt"
    np.savetxt(filename0, KNNgraph_EdgeIndex, delimiter='\t', fmt='%i')  #save as integers. Checked the bidirectional edges.
    
print("All topology structures have been generated!")
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


## Below is for generation of node attribute matrices of cellular spatial graphs.
print("Generating node attribute matrices of KNN graphs...")
cell_type_vec = []
num_nodes = []
for graph_index in range(0, len(region_name_list)):

    region_name = region_name_list.Image[graph_index]
    # Import cell type label.
    CellType_filename = InputFolderName + region_name + "_CellTypeLabel.txt"
    cell_type_label = pd.read_csv(
        CellType_filename,
        sep="\t",  # tab-separated
        header=None,  # no heading row
        names=["cell_type"],  # set our own names for the columns
    )
    cell_type_vec.extend(cell_type_label["cell_type"].values.tolist())
    num_nodes.append(len(cell_type_label))

cell_type_vec_uniq = list(set(cell_type_vec))  # generate a vector of unique cell types and store it to .txt for final illustration.
CellTypeVec_filename = ThisStep_OutputFolderName + "UniqueCellTypeList.txt"
with open(CellTypeVec_filename, 'w') as fp:
    for item in cell_type_vec_uniq:
        # write each item on a new line
        fp.write("%s\n" % item)

max_nodes = math.ceil(max(num_nodes))  # generate the max number of cells and store this value to .txt for the next step.
MaxNumNodes_filename = ThisStep_OutputFolderName + "MaxNumNodes.txt"
with open(MaxNumNodes_filename, 'w') as fp1:
    fp1.write("%i\n" % max_nodes)

# generate a node attribute matrix for each image.
for graph_index in range(0, len(region_name_list)):

    print(f"This is image-{graph_index}")
    region_name = region_name_list.Image[graph_index]
    # import cell type label.
    CellType_filename = InputFolderName + region_name + "_CellTypeLabel.txt"
    cell_type_label = pd.read_csv(
        CellType_filename,
        sep="\t",  # tab-separated
        header=None,  # no heading row
        names=["cell_type"],  # set our own names for the columns
    )

    # initialize a zero-valued numpy matrix.
    node_attr_matrix = np.zeros((len(cell_type_label), len(cell_type_vec_uniq)))
    for cell_ind in range(0, len(cell_type_label)):
        # get the index of the current cell.
        type_index = cell_type_vec_uniq.index(cell_type_label["cell_type"][cell_ind])
        node_attr_matrix[cell_ind, type_index] = 1  # make the one-hot vector for each cell.

    filename1 = ThisStep_OutputFolderName + region_name + "_NodeAttr.txt"
    np.savetxt(filename1, node_attr_matrix, delimiter='\t', fmt='%i')  #save as integers.

print("All node attribute matrices have been generated!")
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


## Below is for transforming input graphs into the data structure required by deep geometric learning. 
print("Start graph data structure transformation...")
# Construct ordinary Python list to hold all input graphs.
data_list = []
for i in range(0, len(region_name_list)):
    region_name = region_name_list.Image[i]

    # Import network topology.
    EdgeIndex_filename = ThisStep_OutputFolderName + region_name + "_EdgeIndex.txt"
    edge_ndarray = np.loadtxt(EdgeIndex_filename, dtype = 'int64', delimiter = "\t")
    edge_index = torch.from_numpy(edge_ndarray)
    #print(edge_index.type()) #should be torch.LongTensor due to its dtype=torch.int64

    # Import node attribute.
    NodeAttr_filename = ThisStep_OutputFolderName + region_name + "_NodeAttr.txt"
    x_ndarray = np.loadtxt(NodeAttr_filename, dtype='float32', delimiter="\t")  #should be float32 not float or float64.
    x = torch.from_numpy(x_ndarray)
    #print(x.type()) #should be torch.FloatTensor not torch.DoubleTensor.
    
    data = Data(x=x, edge_index=edge_index.t().contiguous())
    data_list.append(data)

# Define "SpatialOmicsImageDataset" class based on ordinary Python list.
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

# Create an object of this "SpatialOmicsImageDataset" class.
dataset = SpatialOmicsImageDataset(ThisStep_OutputFolderName, transform=T.ToDense(max_nodes))
print("Step1 done!")
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


