# CytoCommunity

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

### Optional sections 1


### Optional sections 2


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

1.Create a new conda environment using .yml file or .txt file via one of the instructions:

```
conda env create -f environment.yml
conda create --name <env_name> --file requirements.txt
```

You can also install the requirements directly in a conda environment via:

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

1.Create a new conda environment for the program and activate it via the instructions:

```
conda create --name CytoCommunity python=3.10.6
conda activate CytoCommunity
```

2.Install the requirements in the environment with:

```
conda install --file requirements_linux.txt
```

You can also install the dependencies directly via the instructions:

```
conda install pandas
conda install seaborn
conda install pytorch cpuonly -c pytorch
conda install pyg -c pyg
```

## Usage

CytoCommunity can be utilized through both supervised and unsupervised learning. And using CytoCommunity requires five steps:

1.Constructing the KNN gragh.
2.Importing the data acquired from the KNN gragh in step 1.
3.Performing soft clustering through supervised or unsupervised learning.
4.Concensus clustering.
5.Visualization.

#### Running Step0_Construct_KNNgraph.py

#### Running Step1_DataImport.py

#### Running Step2_SoftClusterLearning_Supervised.py

#### Running Step3_ConsensusClustering.R

#### Running Step4_Visualization.py

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

