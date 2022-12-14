# ReDKG
[![Documentation](https://github.com/ShikovEgor/ReDKG/actions/workflows/gh_pages.yml/badge.svg)](https://shikovegor.github.io/ReDKG/)
[![Linters](https://github.com/ShikovEgor/ReDKG/actions/workflows/linters.yml/badge.svg)](https://github.com/ShikovEgor/ReDKG/actions/workflows/linters.yml)
[![Tests](https://github.com/ShikovEgor/ReDKG/actions/workflows/tests.yml/badge.svg)](https://github.com/ShikovEgor/ReDKG/actions/workflows/tests.yml)
<p align="center">
  <img src="https://github.com/ShikovEgor/ReDKG/blob/main/docs/img/logo.png?raw=true" width="300px"> 
</p>


**Re**inforcement learning on **D**ynamic **K**nowledge **G**raphs (**ReDKG**) 
is a toolkit for deep reinforcement learning on dynamic knowledge graphs. 
It is designed to encode static and dynamic knowledge graphs (KG) by constructing vector representations for the entities and relationships. 
The reinforcement learning algorithm based on vector representations is designed to train recommendation models or models of decision support systems based on reinforcement learning (RL) using vector representations of graphs.


## Installation
Python >= 3.9 is required

As a first step, [Pytorch Geometric installation](https://github.com/pyg-team/pytorch_geometric/) and Torch 1.1.2 are required.

#### PyTorch 1.12

```
# CUDA 10.2
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=10.2 -c pytorch
# CUDA 11.3
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
# CUDA 11.6
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.6 -c pytorch -c conda-forge
# CPU Only
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cpuonly -c pytorch
```

When Torch installed clone this repo and run inside repo directory:

```
pip install . 
```

## Donwload test data
Download [ratings.csv](https://grouplens.org/datasets/movielens/20m/) to /data/ folder./
Data folder should contain the following files: 
 - `ratings.csv` - raw rating file;
 - `attributes.csv` - raw attributes file;
 - `kg.txt` - knowledge graph file;
 - `item_index2enity_id.txt` - the mapping from item indices in the raw rating file to entity IDs in the KG file;
### Preprocess the data
```python
from redkg.config import Config
from redkg.preprocess import DataPreprocessor

config = Config()
preprocessor = DataPreprocessor(config)
preprocessor.process_data()
```
### Train model
```python
....
```

---------
<p align="center">
  <img src="https://github.com/ShikovEgor/ReDKG/blob/main/docs/img/lib_schema.png.png?raw=true" width="800px"> 
</p>
More details about first steps with  might be found in the [quick start guide](qwe.asd) and in the [tutorial for novices](qwe.asd).

Project Structure
=================

The latest stable release of  is on the

The repository includes the following directories:
* Package `redkg` contains the main classes and scripts;
* Package `examples` includes several *how-to-use-cases* where you can start to discover how ReDKG works;
* Directory `data` shoul be contains data for modeling;
* All *unit and integration tests* can be observed in the `test` directory;
* The sources of the documentation are in the `docs`.


Cases and examples
==================
To learn representations with default values of arguments from command line, use:
```
python kg_run
```

To learn representations in your own project, use:

```python
from kge import KGEModel
from edge_predict import Evaluator
evaluator = Evaluator()
kge_model = KGEModel(model_name = MODEL_NAME, nentity=nentity, nrelation=nrelation, embedding_size=EMBEDDING_SIZE, gamma=GAMMA, evaluator=evaluator)
```

### Train KGQR model
To train KGQR model on your own data ...
```
...
```

Documentation
=============
Detailed information and description of ReDKG framework is available in the [`Documentation`](https://shikovegor.github.io/ReDKG/)

## Contribution
To contribute this library, the current [code and documentation convention](wiki/Development.md) should be followed.
Project run linters and tests on each pull request, to install linters and testing-packages locally, run 

```
pip install -r requirements-dev.txt
```
To avoid any unnecessary commits please fix any linting and testing errors after running of the each linter:
- `pflake8 .`
- `black .`
- `isort .`
- `mypy stable_gnn`
- `pytest tests`

Contacts
========
- [Contact development team](mailto:egorshikov@itmo.ru)
- Natural System Simulation Team <https://itmo-nss-team.github.io/>

Supported by
============

[National Center for Cognitive Research of ITMO University](https://actcognitive.org/) 

Citation
========
@article{EGOROVA2022284,
title = {Customer transactional behaviour analysis through embedding interpretation},
author = {Elena Egorova and Gleb Glukhov and Egor Shikov},
journal = {Procedia Computer Science},
volume = {212},
pages = {284-294},
year = {2022},
doi = {https://doi.org/10.1016/j.procs.2022.11.012},
url = {https://www.sciencedirect.com/science/article/pii/S1877050922017033}
}

