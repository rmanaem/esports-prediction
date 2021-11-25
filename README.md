# COMP 432

# Authors

- Benjamin Lofo Follo 
- Arman Jahanpour
- Roshleen Mand
- Jialin Yang
# Introduction

## Purpose

This repository holds the code related to the study compiled in the 2021 report *Predictive Analysis in League of Legends e-Sports Matches*, written by the same authors towards the requirements of the COMP 432 Machine Learning class, given to students at Concordia University Montreal's Fall 2021 semester. 

## Deliverable Contents

The deliverable collection contains the following documents:

**Folders**
- `data/`: Resources and files stored from the scripts for data collection
- `ipynb`: Notebook files for data analysis
- `output`: Generated files by the python scripts
- `src`: Executable Python files
- 
**Files**
- `src/fetch_game_ids.py`: Connects to the Riot API to get all game ids from the available tiers and divisions.
- `src/extract_game_data.py`: Scans all `.csv` files inside the output folder, and calls the Riot API to fetch all information related to each match ids, which includes overall game statistics and game timeline.
- `src/processing.ipynb`: Interactive Jupyter Notebook used to Preprocess the data collected inside the `data` folder.
- `src/training.ipynb`: Interactive Jupyter Notebook used to train models against the preprocessed data inside the `data` folder.
  
# Requirements

The following packages are required to ensure all scripts run properly
- sklearn: Provides k-Means library for clustering and vectorizing text
- os: Read the files in the folder specified
  
A Riot API key is also needed for the API Client to work, which you can get here: https://developer.riotgames.com/
# Instructions


1. Fetch the game ids with the following command
```
$ python src/fetch_game_ids.py
```

2. Extract the game data using the following command (NOTE: this step may take very long (ETA:20 hours)
```
$ python src/extract_game_data.py
```

3. Run the `processing.ipynb` to pre-process the data prior to analysis
4. Use the `training.ipynb` file to train the machine learning models
