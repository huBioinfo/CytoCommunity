# CytoCommunity

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

### Optional sections 1


### Optional sections 2


## Install

### Win10

#### Running environment 

CPU: i7

memory: 16G or more

storage：10GB or more

#### Preparing the virtual environment 

Conda version: 22.9.0

Python version: 3.10.6

R version:4.2.1

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

### Linux(centOS7)

#### Running environment 

CPU: i7

memory: 16G or more

storage：10GB or more

#### Preparing the virtual environment 

Conda version: 22.9.0

Python version: 3.10.6

R version: 4.2.0

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

### Run step 0



### Run step 1

### Run step 2

### Run step 3

### Run step 4

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

