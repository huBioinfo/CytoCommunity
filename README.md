# CytoCommunity: a deep graph learning approach for identification of tissue cellular neighborhoods based on cell types and cell spatial distributions

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Overview

How complex cell phenotypes organize and coordinate to support tissue functions remains poorly understood. To understand the complex tissue architecture, the concept of tissue cellular neighborhoods (TCNs) has been proposed as a recurrent functional unit in which different cell types organize and coordinate to support tissue functions. Given a dataset of tissue images from different conditions, it is critical to identify condition-specific TCNs in the images in order to discover tissue spatial structures with biological and clinical relevance. 

We describe the CytoCommunity algorithm for identifying TCNs that can be applied in either an unsupervised or a supervised learning framework.

## Installation

### Hardware environment 

CPU: i7

Memory: 16G or more

Storage: 10GB or more

### Software environment 

Conda version: 22.9.0

Python version: 3.10.6

R version: >= 4.0 suggested

### Windows

#### Preparing the virtual environment

1. Create a new conda environment using .yml file or .txt file with one of the following commands:

```
(base) PS D:\test\CytoCommunity-main> conda env create -f environment.yml
(base) PS D:\test\CytoCommunity-main> conda create --name CytoCommunity --file requirements.txt
```

Note that the command should be executed in the parent directory of the .yml or .txt file. And if you use the .txt file, please convert it to UTF-8 format.

2. The requirements can also be installed directly in a new conda environment via:

```
(base) PS C:\Users\Lenovo> conda create --name CytoCommunity pyhton=3.10.6
(base) PS C:\Users\Lenovo> conda activate CytoCommunity
(CytoCommunity) PS C:\Users\Lenovo> conda install --yes --file requirements.txt
```

3. Install package diceR (R has already been included in the requirements) with:

```
(CytoCommunity) PS C:\Users\Lenovo> R.exe
> install.packages("diceR")
```

### Linux

#### Preparing the virtual environment 

1. Create a new conda environment using .yml file and activate it with:

```
(base) conda env create -f environment_linux.yml
(base) conda activate CytoCommunity
```
2. Install R and package diceR via:

```
(CytoCommunity) conda install R
(CytoCommunity) R
> install.packages("diceR")
```

## Usage

CytoCommunity can be utilized in either an unsupervised or a supervised learning framework. You can apply CytoCommunity algorithm in the following five steps:

  1. Step0: Constructing KNN graghs.

  2. Step1: Importing data.

  3. Step2: Performing soft clustering through supervised or unsupervised learning.

  4. Step3: Concensus clustering for more robust result.

  5. Step4: Visualization of the clustering result.

### Unsupervised CytoCommunity

The input data of the unsupervised learning part of CytoCommunity algorithm is information of MERFISH Brain KNN graph, including cell type label, coordinates, edge index, gragh index and node attributes files and a image name list, seen in the folder "MERFISH_Brain_KNNgraph_Input".

Here comes the running process in Windows Powershell:

#### 1. Step0_Construct_KNNgraph.py

Use step 0 to construct KNN graghs and prepare data for the following steps.

```
(base) PS C:\Users\Lenovo> conda activate CytoCommunity
(CytoCommunity) PS C:\Users\Lenovo> cd D:\test\CytoCommunity-main\Unsupervised_CytoCommunity
(CytoCommunity) PS D:\test\CytoCommunity-main\Unsupervised_CytoCommunity> python Step0_Construct_KNNgraph.py
```

#### 2. Step1_DataImport.py

Step 1 is data preprocessing to convert the input data to the standard format of torch. The running result includes two folders, "processed" and "raw", with the former containing three .pt files, named pre_filter, pre_transform and SpatialOmicsImageDataset, and the latter nothing. 

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Unsupervised_CytoCommunity> python Step1_DataImport.py
```

#### 3. Step2_SoftClusterLearning_Unsupervised.py

In step 2, CytoCommunity performs soft clustering through unsupervised learning. For each epoch of the training process, step 2 generates a folder that contains cluster adjacent matrix, cluster assign matrix, node mask, and gragh index files and a training loss file.

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Unsupervised_CytoCommunity> python Step2_SoftClusterLearning_Unsupervised.py
```

#### 4. Step3_ConsensusClustering.R

To make the soft clustering result more robust, step 3 is consensus clustering using R, with file "ConsensusLabel_MajorityVoting.csv" generated to show the result. Make sure that package diceR has been installed.

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Unsupervised_CytoCommunity> Rscript.exe Step3_ConsensusClustering.R
```

#### 5. Step4_Visualization.py

Visualization of the consensus clustering result is the final step of CytoCommunity algorithm. After this step, we'll eventually get the gragh of tissue cellular neighborhood(TCN).

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Unsupervised_CytoCommunity> python Step4_Visualization.py
```

### Supervised CytoCommunity

On the other hand, we can also use CytoCommunity algorithm through supervised learning. The input data of this part is information of codex colon cancer KNN graph, including a image name list and cell type label, coordinates, edge index, gragh index, gragh label and node attributes files, seen in the folder "CODEX_ColonCancer_KNNgraph_Input".

Here comes the running process in Windows Powershell:

#### 1. Step0_Construct_KNNgraph.py

Use step 0 to construct KNN graghs and prepare data for the following steps.

```
(base) PS C:\Users\Lenovo> conda activate CytoCommunity
(CytoCommunity) PS C:\Users\Lenovo> cd D:\test\CytoCommunity-main\Supervised_CytoCommunity
(CytoCommunity) PS D:\test\CytoCommunity-main\Supervised_CytoCommunity> python Step0_Construct_KNNgraph.py
```

#### 2. Step1_DataImport.py

Step 1 is for data preprocessing, converting the input data to the standard format of torch. The running result includes two folders, "processed" and "raw", with the former containing three .pt files, named pre_filter, pre_transform and SpatialOmicsImageDataset, and the latter nothing.

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Supervised_CytoCommunity> python Step1_DataImport.py
```

#### 3. Step2_SoftClusterLearning_Supervised.py

CytoCommunity uses step 2 to perform soft clustering through supervised learning. For each Fold in each Time of the training process, this step generates a folder that contains cluster adjacent matrix, cluster assign matrix, gragh index, and node mask files and a training loss file.

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Supervised_CytoCommunity> python Step2_SoftClusterLearning_Supervised.py
```

#### 4. Step3_ConsensusClustering.R

In this step, we'll get a image collection folder that contains cluster assign matrix, node mask, gragh index and consensus label files of each Fold in each Time of the training process. Note that package diceR should be installed first. 

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Supervised_CytoCommunity> Rscript.exe Step3_ConsensusClustering.R
```

#### 5. Step4_Visualization.py

After the final step, TCN results got. 

```
(CytoCommunity) PS D:\test\CytoCommunity-main\Supervised_CytoCommunity> python Step4_Visualization.py
```

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

