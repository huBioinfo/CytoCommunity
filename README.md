![header](support/logo.png)   

# Unsupervised and supervised discovery of tissue cellular neighborhoods from cell phenotypes with CytoCommunity


### _2025-04-10: We are excited to annouce an extended version "CytoCommunity+" (https://github.com/huBioinfo/CytoCommunity-plus)._
#### _Advantages of CytoCommunity+:_
#### _(1) Using significantly less memory for large-scale spatial omics samples with millions of cells._
#### _(2) A unified weakly-supervised model applicable for both multi-condition and single-condition datasets._
#### _(3) High TCN alignment performance makes it well-suited for large cohort studies._



## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Update Log](#update-log)
- [Maintainers](#maintainers)
- [Citation](#citation)


## Overview

<div align=center><img src="https://github.com/huBioinfo/CytoCommunity/blob/main/support/Schematic_Diagram.png" width="650" height="650" alt="pipline"/></div>  


It remains poorly understood how different cells in a tissue organize and coordinate with each other to support tissue functions. To better understand the structure-function relationship of a tissue, the concept of **tissue cellular neighborhoods (TCNs) or spatial domains** as well as their identification tools have been proposed. However, **several limitations include:**

(1) Most existing methods are originally designed for spatial transcriptomics data and thus use expression of hundreds or thousands of genes as features to infer TCNs. Such methods may not be applicable to spatial proteomics data that only have a few tens of protein expression features available.

(2) Using gene expression data as input cannot directly establish the relationship between cell types and TCNs in a tissue, making the interpretation of TCNs challenging.

(3) Given a cohort of tissue samples associated with different conditions (e.g., disease risk and patient prognosis), it is important to identify condition-specific TCNs with more biological and clinical relevance (e.g., tertiary lymphoid structure (TLS), which is typically present in low-risk but not in high-risk patients of many cancer types). Most existing methods are designed to detect TCNs in individual tissue samples by unsupervised learning and thus not applicable for the identification of condition-specific TCNs de novo. 

We developed this tool, named **CytoCommunity**, for identifying TCNs that can be applied in **either unsupervised or weakly-supervised** fashion. We formulate TCN identification as a community detection problem on graphs and employ a graph neural network (GNN) model to identify TCNs. **Several advantages include:**

(1) CytoCommunity directly uses cell phenotypes as features to learn TCN partitions and thus facilitates the interpretation of TCN functions. 

(2) CytoCommunity can not only infer TCNs for individual samples (unsupervised mode), but also identify **condition-specific TCNs** from a cohort of labeled tissue samples by leveraging differentiable graph pooling and sample labels (supervised mode), which is an effective strategy to address the difficulty of graph alignment across samples.


**_Highlights on the differences of TCNs identified by the two learning modes:_**

**_1) TCNs are identified per sample/image using the unsupervised mode and thus TCNs from different samples/images are NOT aligned._**

**_2) TCNs are identified in all samples/images simultaneously using the weakly-supervised mode and thus TCNs from different samples/images are automatically aligned._**


## Installation

### Hardware requirement 

CPU: i7

Memory: 16G or more

Storage: 10GB or more

### Software requirement

Conda version: 22.9.0

Python version: 3.10.6

R version: >= 4.0 suggested

Clone this repository and cd into it as below.
```
git clone https://github.com/huBioinfo/CytoCommunity.git
cd CytoCommunity
```

### Set up virtual environment for Windows

1. Create a new conda environment using the environment.yml file (CPU version):

    ```bash
    conda env create -f environment.yml
    ```

    Or create a new conda environment using the environment_windows_gpu.yml file (GPU version):

    ```bash
    conda env create -f environment_windows_gpu.yml
    ```


2. Install the diceR package (R has already been included in the requirements) with the following command:

    ```bash
    R.exe
    > install.packages("diceR")
    ```

### Set up virtual environment for Linux

1. Create a new conda environment using the environment_linux.yml file (CPU version):

    ```bash
    conda env create -f environment_linux.yml
    ```

    Or create a new conda environment using the environment_linux_gpu.yml file (GPU version):

    ```bash
    conda env create -f environment_linux_gpu.yml
    ```


2. Install R and the diceR package:
    
    ```bash
    conda install R
    R
    > install.packages("diceR")
    ```

The whole installation should take around 20 minutes.


## Usage

The CytoCommunity algorithm for TCN indentification can be used in either an unsupervised or a supervised learning mode. You can reproduce TCN partitions shown in the published CytoCommunity paper using the commands below. The associated code scripts and example input data can be found under the directory "Tutorial/".

### _Unsupervised CytoCommunity_

### Prepare input data

The example input data to the unsupervised learning mode of CytoCommunity is derived from a mouse brain MERFISH dataset generated by Moffitt et al. (Science, 2018), including **three types of files: (1) cell type label and (2) cell spatial coordinate files for each sample/image, as well as (3) an image name list file**. These example input files can be found under the directory "Tutorial/Unsupervised/MERFISH-Brain_Input/".

Note that the naming fashion of the three types of files cannot be changed when using your own data. These files should be named as **"[image name]_CellTypeLabel.txt", "[image name]_Coordinates.txt" and "ImageNameList.txt"**. Here, [image_name] should be consistent with your customized image names listed in the "ImageNameList.txt". The "[image name]_CellTypeLabel.txt" and "[image name]_Coordinates.txt" list cell type names and cell coordinates (tab-delimited x/y) of all cells in an image, respectively. The cell orders should be exactly the same across the two files.

### Ready to run

#### 1. Use Step1 to construct KNN-based cellular spatial graghs and convert the input data to the standard format required by Torch.

This step generates a folder "Step1_Output" including constructed cellular spatial graphs of all samples/images in your input dataset folder (e.g., /MERFISH-Brain_Input/). No need to re-run this step for different images.

```bash
conda activate CytoCommunity
cd Tutorial/Unsupervised
python Step1_ConstructCellularSpatialGraphs.py
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset.
- KNN_K: The K value used in the construction of the K nearest neighbor graph (cellular spatial graph) for each sample/image. This value can be empirically set to the integer closest to the square root of the average number of cells in the images in your dataset.

#### 2. Use Step2 to perform soft TCN assignment learning in an unsupervised fashion.

This step generates a folder "Step2_Output_[specified image name]" including multiple runs (subfolders) of soft TCN assignment learning module. Each subfolder contains a cluster adjacent matrix, a cluster assignment matrix (soft TCN assignment matrix), a node mask file and a loss recording file. You need to re-run this step for different images by changing the hyperparameter "Image_Name".

```bash
python Step2_TCNLearning_Unsupervised.py
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset, consistent with Step1.
- Image_Name: The name of the sample/image on which you want to identify TCNs.
- Num_TCN: The maximum number of TCNs you expect to identify.
- Num_Run: How many times to run the soft TCN assignment learning module in order to obtain robust results. [Default=20]
- Num_Epoch: The number of training epochs. This value can be smaller than the default value [3000] for the large image (e.g., more than 10,000 cells).
- Embedding_Dimension: The dimension of the embedding features for each cell. [Default=128]
- Learning_Rate: This parameter determines the step size at each iteration while moving toward a minimum of a loss function. [Default=1E-4]
- Loss_Cutoff: An empirical cutoff of the final loss to avoid underfitting. This value can be larger than the default value [-0.6] for the large image (e.g., more than 10,000 cells).

#### 3. Use Step3 to perform TCN assignment ensemble.

The result of this step is saved in the "Step3_Output_[specified image name]/TCNLabel_MajorityVoting.csv" file. Make sure that the diceR package has been installed before Step3. You need to re-run this step for different images by changing the hyperparameter "Image_Name".

```bash
Rscript Step3_TCNEnsemble.R
```
&ensp;&ensp;**Hyperparameters**
- Image_Name: The name of the sample/image on which you want to identify TCNs, consistent with Step2.

#### 4. Use Step4 to visualize single-cell spatial maps colored based on cell type annotations and final TCN partitions.

This step generates a folder "Step4_Output_[specified image name]" including two plots of this single-cell spatial map (in PNG and PDF formats) colored by input cell type annotations and identified TCNs, respectively. A "ResultTable_[specified image name].csv" file is also genereated to store the detailed information of this single-cell spatial map. You need to re-run this step for different images by changing the hyperparameter "Image_Name".

```bash
python Step4_ResultVisualization.py
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset, consistent with Step1.
- Image_Name: The name of the sample/image on which you want to identify TCNs, consistent with Step2.

### _Weakly-supervised CytoCommunity_

### Prepare input data

The example input data to the supervised learning mode of CytoCommunity is derived from a triple-negative breast cancer (TNBC) MIBI-TOF dataset generated by Keren et al. (Cell, 2018), including **four types of files: (1) cell type label and (2) cell spatial coordinate and (3) graph (sample) label files for each sample/image, as well as (4) an image name list file**. These example input files can be found under the directory "Tutorial/Supervised/MIBI-TNBC_Input/".

Note that the naming fashion of the four types of files cannot be changed when using your own data. These files should be named as **"[image name]_CellTypeLabel.txt", "[image name]_Coordinates.txt", "[image name]_GraphLabel.txt" and "ImageNameList.txt"**. Here, [image_name] should be consistent with your customized image names listed in the "ImageNameList.txt". The "[image name]_CellTypeLabel.txt" and "[image name]_Coordinates.txt" list cell type names and cell coordinates (tab-delimited x/y) of all cells in an image, respectively. The cell orders should be exactly the same across the two files. Different from unsupervised version, supervised CytoCommunity requires the "[image name]_GraphLabel.txt", where lists an integer (like "0", "1", "2", etc) to describe the graph/sample/image label.

### Ready to run

#### 1. Use Step1 to construct KNN-based cellular spatial graghs and convert the input data to the standard format required by Torch.

This step generates a folder "Step1_Output" including constructed cellular spatial graphs of all samples/images in your input dataset folder (e.g., /MIBI-TNBC_Input/).

```bash
conda activate CytoCommunity
cd Tutorial/Supervised
python Step1_ConstructCellularSpatialGraphs.py
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset.
- KNN_K: The K value used in the construction of the K nearest neighbor graph (cellular spatial graph) for each sample/image. This value can be empirically set to the integer closest to the square root of the average number of cells in the images in your dataset.

#### 2. Use Step2 to perform soft TCN assignment learning in a supervised fashion.

This step generates a folder "Step2_Output", including results ("Time" folder) of running the soft TCN assignment learning module using the 10 times of 10-fold cross-validation fashion. Each "Time" folder contains results ("Fold" folder) of one time of 10-fold cross-validation. Each "Fold" folder contains cluster assignemnt matrix (soft TCN assignment matrix) files for all images.

```bash
python Step2_TCNLearning_Supervised.py
```
&ensp;&ensp;**Hyperparameters**
- Num_TCN: The maximum number of TCNs you expect to identify.
- Num_Times: How many times to run the cross-vadlidation independently. [Default=10]
- Num_Folds: The k value in the k-fold cross-validation. [Default=10]
- Num_Epoch: The number of training epochs. [Default=100]
- Embedding_Dimension: The dimension of the embedding features for each cell. [Default=512]
- MiniBatchSize: This value is commonly set to be powers of 2 due to efficiency consideration. In the meantime, this value is suggested to be closest to half sizes of the training sets. [Default=16]
- Learning_Rate: This parameter determines the step size at each iteration while moving toward a minimum of a loss function and should be increased with the mini-batch size increase. [Default=1E-4]
- beta: A weight parameter to balance the MinCut loss used for graph partitioning and the cross-entropy loss used for graph classification. The default value is set to [0.9] due to emphasis on graph partitioning.

#### 3. Use Step3 to perform TCN assignment ensemble.

The results of this step are saved under the "Step3_Output/ImageCollection/" directory. A "TCNLabel_MajorityVoting.csv" file will be generated for each image. Make sure that the diceR package has been installed before Step3.

```bash
Rscript Step3_TCNEnsemble.R
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset, consistent with Step1.

#### 4. Use Step4 to visualize single-cell spatial maps colored based on cell type annotations and final TCN partitions.

This step generates a folder "Step4_Output" including three subfolders. The "CellType_Plot" subfolder stores single-cell spatial maps of all images (in PNG and PDF formats) colored by input cell type annotations. The "TCN_Plot" subfolder stores single-cell spatial maps of all images (in PNG and PDF formats) colored by identified TCNs. The "ResultTable_File" subfolder stores detailed information of single-cell spatial maps of all images in CSV format.

```bash
python Step4_ResultVisualization.py
```
&ensp;&ensp;**Hyperparameters**
- InputFolderName: The folder name of your input dataset, consistent with Step1.


## Update Log

2024-01-08: The latest release “CytoCommunity\_v1.1.0” (main branch) makes the input data easier to prepare, compared to the original version v1.0.0.


## Maintainers

Yuxuan Hu (huyuxuan@xidian.edu.cn)

Liukang Wu (yetong@stu.xidian.edu.cn)

Yafei Xu (22031212416@stu.xidian.edu.cn)

Kai Tan (tank1@chop.edu)


## Citation

Yuxuan Hu, Jiazhen Rong, Yafei Xu, Runzhi Xie, Jacqueline Peng, Lin Gao, Kai Tan. Unsupervised and supervised discovery of tissue cellular neighborhoods from cell phenotypes. **Nature Methods**, 2024, https://doi.org/10.1038/s41592-023-02124-2.


