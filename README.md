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

CPU: i7

memory: 16G or more

storage：10GB or more

#### Preparing the virtual environment 

Conda version: 22.9.0

Python version: 3.10.6

Create a conda environment for cyto:

```
conda env create -f environment.yml
```

Or

```
conda create --name <env_name> --file requirements.txt
```

Or install the requirements in the existing environment directly:

```
$ conda install --yes --file requirements.txt
```
### Linux(centOS7)

CPU: i7

memory: 16G or more

storage：10GB or more

#### Preparing the virtual environment 

Conda version: 22.9.0

Python version: 3.10.6

Create a new conda environment:

```
conda create --name cyto python=3.10.6
```

Install the requirements:

```
conda install --file requirements_linux.txt
```

Or Install the dependencies directly:

```
conda install pandas
conda install seaborn
conda install pytorch cpuonly -c pytorch
conda install pyg -c pyg
```

## Usage

```
```

## Maintainers

[@HuBioinfo](https://github.com/huBioinfo)(huyuxuan@xidian.edu.cn)

[@yafeixu-xidian](https://github.com/yafeixu-xidian)(22031212416@stu.xidian.edu.cn)

## Contributing

Feel free to dive in!

## License

