![header](support/logo.png)   

# CytoCommunity: a deep graph learning approach for identification of tissue cellular neighborhoods based on cell phenotypes and cell spatial distributions

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Overview

![overview](support/overview.png)

It remains poorly understood how different cell phenotypes organize and coordinate with each other to support tissue functions. To better understand the structure-function relationship of a tissue, the concept of tissue cellular neighborhoods (TCNs) has been proposed. Furthermore, given a set of tissue images associated with different conditions, it is often desirable to identify condition-specific TCNs with more biological and clinical relevance. However, there is a lack of computational tools for de novo identification of condition-specific TCNs by explicitly utilizing tissue image labels. 

We developed the CytoCommunity algorithm for identifying TCNs that can be applied in either an unsupervised or a supervised learning framework. The direct usage of cell phenotypes as initial features to learn TCNs makes it applicable to both single-cell transcriptomics and proteomics data and facilitates the interpretation of TCN functions as well. Additionally, CytoCommunity can not only infer TCNs for individual images but also identify condition-specific TCNs for a set of images by leveraging graph pooling and image labels, which effectively addresses the challenge of TCN alignment across images.

CytoCommunity is the first computational tool for end-to-end unsupervised and supervised analyses of single-cell spatial maps and enables direct discovery of conditional-specific cell-cell communication patterns across variable spatial scales.

## Installation

### Hardware requirement 

CPU: i7

Memory: 16G or more

Storage: 10GB or more

### Software requirement

Conda version: 22.9.0

Python version: 3.10.6

R version: >= 4.0 suggested

### For Windows

#### Preparing the virtual environment

1. Create a new conda environment using the environment.yml file or the requirements.txt file with one of the following commands:

    ```bash
    conda env create -f environment.yml
    # or
    conda create --name CytoCommunity --file requirements.txt
    ```

Note that the command should be executed in the parent directory of the environment.yml or requirements.txt file. And if you use the .txt file, please convert it to the UTF-8 format.

2. The requirements can also be installed directly in a new conda environment:

    ```bash
    conda create --name CytoCommunity pyhton=3.10.6
    conda activate CytoCommunity
    conda install --yes --file requirements.txt
    ```

3. Install the diceR package (R has already been included in the requirements) with the following command:

    ```bash
    R.exe
    > install.packages("diceR")
    ```

### For Linux

#### Preparing the virtual environment 

1. Create a new conda environment using the environment_linux.yml file and activate it:

    ```bash
    conda env create -f environment_linux.yml
    conda activate CytoCommunity
    ```

2. Install R and the diceR package:
    
    ```bash
    conda install R
    R
    > install.packages("diceR")
    ```
    
## Usage

CytoCommunity can be used in either an unsupervised or a supervised learning mode. You can apply CytoCommunity algorithm in the following five steps:

  1. Step0: Constructing KNN graghs.

  2. Step1: Importing data.

  3. Step2: Performing soft clustering through supervised or unsupervised learning.

  4. Step3: Concensus clustering for more robust result.

  5. Step4: Visualization of the concensus clustering result.

### Unsupervised CytoCommunity

The example input data to the unsupervised learning mode of CytoCommunity is a KNN graph based on mouse brain MERFISH data, including cell type labels, cell spatial coordinates, edge index, gragh index and node attributes files and an image name list. These files can be found in the folder "MERFISH_Brain_KNNgraph_Input".

Running steps in Windows Powershell:

#### 1. Step0_Construct_KNNgraph.py

Use step0 to construct KNN graghs and prepare data for the subsequent steps.

```bash
conda activate CytoCommunity
cd D:\test\CytoCommunity-main\Unsupervised_CytoCommunity
python Step0_Construct_KNNgraph.py
```

#### 2. Step1_DataImport.py

Step1 conducts data preprocessing to convert the input data to the standard format of torch. It produces two file folders, "processed" and "raw", with the former containing three .pt files, named as pre_filter, pre_transform and SpatialOmicsImageDataset, and the latter being an empty folder at this point. 

```bash
python Step1_DataImport.py
```
    
#### 3. Step2_SoftClusterLearning_Unsupervised.py

In step2, CytoCommunity performs soft clustering based on unsupervised learning. For each epoch of the training process, step2 generates a folder that contains cluster adjacent matrix, cluster assignment matrix, node mask, and gragh index files and a training loss file.

```bash
python Step2_SoftClusterLearning_Unsupervised.py
```

#### 4. Step3_ConsensusClustering.R

To make the soft clustering result more robust, step3 performs consensus clustering using R. The result is saved in the "ConsensusLabel_MajorityVoting.csv" file. Make sure that the diceR package has been installed before step3.

```bash
Rscript.exe Step3_ConsensusClustering.R
```

#### 5. Step4_Visualization.py

The consensus clustering result is summarizied and visualized in this step. After this step, we will obtain the gragh of tissue cellular neighborhood(TCN).

```bash
python Step4_Visualization.py
```

### Supervised CytoCommunity

We can also run CytoCommunity as a supervised learning task. The example input data to this part is a KNN graph based on colon cancer CODEX data, including a image name list and cell type label, cell spatial coordinates, edge index, gragh index, gragh label and node attributes files, all of which are stored in the folder "CODEX_ColonCancer_KNNgraph_Input".

Running steps in Windows Powershell:

#### 1. Step0_Construct_KNNgraph.py

Use step0 to construct KNN graghs and prepare data for the subsequent steps.

```bash
conda activate CytoCommunity
cd D:\test\CytoCommunity-main\Supervised_CytoCommunity
python Step0_Construct_KNNgraph.py
```

#### 2. Step1_DataImport.py

Step1 conducts data preprocessing to convert the input data to the standard format of torch. It produces two file folders, "processed" and "raw", with the former containing three .pt files, named as pre_filter, pre_transform and SpatialOmicsImageDataset, and the latter being an empty folder at this point. 

```bash
python Step1_DataImport.py
```

#### 3. Step2_SoftClusterLearning_Supervised.py

Step2 performs soft clustering based on supervised learning. For each fold in each round of the training process, this step generates a folder that contains cluster adjacent matrix, cluster assignment matrix, gragh index, and node mask files and a training loss file.

```bash
python Step2_SoftClusterLearning_Supervised.py
```

#### 4. Step3_ConsensusClustering.R

For each image, Step3 generates the following files: cluster assign matrix, node mask, gragh index and consensus label files of each fold in each run of the training process. Note the diceR package should be installed before this step. 

```bash
Rscript.exe Step3_ConsensusClustering.R
```

#### 5. Step4_Visualization.py

The result is summarizied and visualized in this step. After this step, we will obtain graghs of tissue cellular neighborhoods (TCNs) associated with each condition.

```bash
python Step4_Visualization.py
```

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

