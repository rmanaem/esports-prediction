# Esports Prediction

## Abstract

League of Legends is a team-based strategy game requiring several skills to achieve victories. Predicting a winner from a given match can prove to be difficult, as several traits hold a level of importance to determining the victor. The study analyzes key parameters of a given match, such as overall statistics, objective first and game resources at a given time. From a set point in time, classification models (support vector machine, random forest and k-nearest neighbours to name a few) were trained against the most important features assessed using their correlation values. The prediction of a victor can be maximized to the point it surpasses a uniform random distribution; relying on parameters such that weights are properly distributed can further improve the model’s results.

---

## Introduction

League of Legends is a multiplayer online battle arena (MOBA) game where two teams of five players face off to destroy the other’s base [1]. While the computerized sport possesses the luxury of providing instantly measurable data, analysts may find it difficult to predict the outcome of a match, due to the number of parameters that can fluctuate from one game to another, along with multiple factors that may influence the results. Through this study, we aim to attempt at maximizing the likelihood of predicting the victory of one League of Legends team over another and observe how machine learning can solve the problem in providing a good assessment of a team’s strength based on the information it is provided throughout a match.

---

## Data Overview

### League of Legends

Created in 2009 by Riot Games, League of Legends (LoL) is a team-based strategy game involving two teams aiming to destroy their opponent’s base. Before the start of the game players select one of over 150 unique champions, each with their own play style and abilities, to build a team that fits their desired game plan and strategy.

A match of League of Legends requires several skills to achieve success: a player must be skillful in generating income by increasing their Creep Score (CS), taking down enemy champions and turrets, as well as controlling important map resources such as elemental drakes and Baron Nashor. Predicting a winner from a given match can prove to be difficult, as each of these traits can tip a match’s outcome to a team’s favour and how these milestones are accomplished is just as important as completing them.

---

## Deliverable Contents

The deliverable collection contains the following documents:

**Folders**

- `data/`: Resources and files stored from the scripts for data collection
- `data/json`: Example Endpoint Responses for the Riot API that are analyzed by `extract_game_data.py`
- `data/processed`: Final CSV training data set
- `data/raw`: Unprocessed files created by `extract_game_data.py`
- `data/csv`: List of match ids generated by `fetch_game_ids.py`
- `src/`: Executable Python files
- `src/models/`: Joblib files for the models that have been trained by our ipynb file
- `src/parsers/`: Parsers used within `extract_game_data.py` to prepare digestable tuple instances
- `src/services/`: API scripts to communicate with third-party data services

**Files**

- `src/fetch_game_ids.py`: Connects to the Riot API to get all game ids from the available tiers and divisions.
- `src/extract_game_data.py`: Scans all `.csv` files inside the output folder, and calls the Riot API to fetch all information related to each match ids, which includes overall game statistics and game timeline.
- `src/processing.ipynb`: Interactive Jupyter Notebook used to Preprocess the data collected inside the `data` folder.
- `src/training.ipynb`: Interactive Jupyter Notebook used to train models against the preprocessed data inside the `data` folder.
  
# Requirements

The following packages are required to ensure all scripts run properly

- sklearn: Provides k-Means library for clustering and vectorizing text
- os: Read the files in the folder specified
  
A Riot API key is also needed for the API Client to work, which you can get here: <https://developer.riotgames.com/>

# Instructions

1. Fetch the game ids with the following command

```
python src/fetch_game_ids.py
```

2. Extract the game data using the following command **(NOTE: this step may take very long (ETA:20 hours)**

```
python src/extract_game_data.py
```

3. Run the `processing.ipynb` to pre-process the data prior to analysis
4. Use the `training.ipynb` file to train the machine learning models

# Thank you

We have used these sources for bringing the project to life:

*AlphaStar: Grandmaster level in StarCraft II using multi-agent reinforcement learning* (For formatting layout of our report)
<https://deepmind.com/blog/article/AlphaStar-Grandmaster-level-in-StarCraft-II-using-multi-agent-reinforcement-learning>

*Riot Developer - Collecting data* (Best practices on the Riot API)
<https://riot-api-libraries.readthedocs.io/en/latest/collectingdata.html>
