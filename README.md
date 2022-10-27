# CytoCommunity

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

## Installation

### Windows

#### Hardware environment 

CPU: i7

Memory: 16G or more

Storage: 10GB or more

#### Software environment 

Conda version: 22.9.0

Python version: 3.10.6

R version: 4.2.1

#### Preparing the virtual environment

1. Create a new conda environment using .yml file or .txt file via one of the instructions:

```
conda env create -f environment.yml
conda create --name <env_name> --file requirements.txt
```

2. You can also install the requirements directly in a new conda environment with:

```
conda create --name CytoCommunity pyhton=3.10.6
conda activate CytoCommunity
conda install --yes --file requirements.txt
```

### Linux

#### Hardware environment 

CPU: i7

Memory: 16G or more

Storage: 10GB or more

#### Software environment 

Conda version: 22.9.0

Python version: 3.10.6

R version: 4.2.0

#### Preparing the virtual environment 

1. Create a new conda environment for the program and activate it via the instructions:

```
conda create --name CytoCommunity python=3.10.6
conda activate CytoCommunity
```

2. Install the requirements in the environment with:

```
conda install --file requirements_linux.txt
```

3. You can also install the dependencies directly via the instructions:

```
conda install pandas
conda install seaborn
conda install pytorch cpuonly -c pytorch
conda install pyg -c pyg
```

## Usage

CytoCommunity can be utilized through both supervised and unsupervised learning. You can apply CytoCommunity in the following five steps:

  1. Step0: Constructing the KNN gragh.

  2. Step1: Importing data from the KNN gragh in 1.

  3. Step2: Performing soft clustering through supervised or unsupervised learning.

  4. Step3: Concensus clustering.

  5. Step4: Visualization of the result of clustering in 4.

### Unsupervised CytoCommunity

The input data of the unsupervised learning part of the CytoCommunity algorithm is for MERFISH Brain KNN graph, including a image name list and cell type label, coordinates, edge index, gragh index and node attributes of cells, seen in the folder "MERFISH_Brain_KNNgraph_Input".

1. Step0_Construct_KNNgraph.py

Use step 0 to construct KNN gragh and prepare data for the following steps.

2. Running Step1_DataImport.py

The running result of step 1 includes two folders, "processed" and "raw", with the former consisting of three .pt files and the latter none. 

3. Running Step2_SoftClusterLearning_Unsupervised.py

4. Running Step3_ConsensusClustering.R

5. Running Step4_Visualization.py

### Supervised CytoCommunity

The input data of the supervised learning part of the CytoCommunity algorithm is for codex colon cancer KNN graph, including a image name list and cell type label, coordinates, edge index, gragh index, gragh label and node attributes of cells, seen in the folder "CODEX_ColonCancer_KNNgraph_Input".

1. Running Step0_Construct_KNNgraph.py

2. Running Step1_DataImport.py

3. Running Step2_SoftClusterLearning_Supervised.py

4. Running Step3_ConsensusClustering.R

5. Running Step4_Visualization.py

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

