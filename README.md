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

<p alt="map" align="center"><a href="https://github.com/rmanaem/esports-prediction/blob/master/figures/map.png"><img src="https://github.com/rmanaem/esports-prediction/blob/master/figures/map.png?raw=true"/></a></p>

A match of League of Legends requires several skills to achieve success: a player must be skillful in generating income by increasing their Creep Score (CS), taking down enemy champions and turrets, as well as controlling important map resources such as elemental drakes and Baron Nashor. Predicting a winner from a given match can prove to be difficult, as each of these traits can tip a match’s outcome to a team’s favour and how these milestones are accomplished is just as important as completing them.

### Definitions

Our study will focus on analyzing key parameters of a given match and their development on a minute-to-minute basis. Using the Riot API provided by the game publishers, over 40000 matches and 1.3 million frames of games that have occurred in the year of 2021 have been compiled for analysis. A few terms must be introduced to properly understand the conclusions that stem from our evaluations.

#### Match

A match object contains overall statistics of the contest between the two teams, such as game duration, the winning team of the game; it also records statistics for each of its game participants. For the purpose of this study, only the winning team will serve as the output of our results.

#### Objective Firsts

Objectives are key milestones teams can achieve during a match. These can vary from destroying structures to defeating elite monsters or opposing participants. A match object provides to us which team has been able to attain each of these key milestones for the first time in that game:

- Champion: The first player succeeding to defeat another player in a game is awarded bonus gold to the team, giving them an edge at the early stages of the game. This is commonly referred to as ”first blood”.
- Turret (or Tower): Bonus gold is rewarded for every team member that contributed to the destruction of the first structure.
- Dragon: When slain, it rewards the team with a buff on all its players for the remainder of the game.
- Baron Nashor: A team successfully slaying Baron Nashor is rewarded with a buff on all team players active on the map Baron only becomes available after 20 minutes has elapsed in a game, making it a potential advantage to be acquired from the mid to the late stages of the game.
- Inhibitor: When an inhibitor is destroyed, the opposing team produces stronger minions for a set amount of time, giving them added advantage at the later stages of the game.

#### Frame and Game Resources

A frame f represents the current state of a match at the given minute mark. The cumulated amounts for each team player’s stat line is compiled under a feature specific to that team. This will include several dimensions such as:
- Creep Score (CS) and gold collected
- Total damage done to champions
- Total champion kills by the team
- Amount of turrets, inhibitors and plates destroyed
- Amount of Baron Nashors slain
- Amount of Rift Heralds slain

### Feature Analysis

With the number of features at our disposal, it is worthwhile to explore and analyze how they relate to our expected outcome and their importance to our study. From analyzing five objective first features analyzed, the first inhibitor property came out as the strongest indicator to a winner, with 90% of the matches won by the same team that has destroyed the first inhibitor. This is plausible, as inhibitors are broken late into a game’s match and give an advantageous boost to the team towards reaching a decisive win. The figure below illustrates proportion of matches won according to the team that acquired the first inhibitors.

<p alt="first-inhibitor" align="center"><a href="https://github.com/rmanaem/esports-prediction/blob/master/figures/first-inhibitor.png"><img src="https://github.com/rmanaem/esports-prediction/blob/master/figures/first-inhibitor.png?raw=true"/></a></p>

On the game resources side, A strong correlation was shared between the winning team, the gold advantage and the kill advantage. As gold is the primary indicator of a team’s strength, it follows that it stands as a strong measure to determine which team has the best chance of cracking the opponent’s base.

| Feature | Value |
| ----------- | ----------- |
| gold advantage | 0.717 |
| kill advantage | 0.647 |
| tower advantage | 0.578 |
| cs advantage | 0.509 |
| dragon advantage | 0.507 |
| baron advantage | 0.417 |
| inhibitor advantage | 0.414 |
| plate advantage | 0.375 |
| rift advantage | 0.247 |

In sum, the data holds clear levers that the model can use for coming up with a decision as to solving the classification problem. The choice of the data points at a particular time frame in every game will be a determining factor for achieving adequate results during evaluation. To solve the training set’s dimensionality problem, a correlation threshold was set to remove any features that lie below a ratio of 0.5; this left us with the following features remained after the reduction: first inhibitor, baron, kill, gold, damage, and tower advantage.

---

## Learning Algorithms

### Models

The following algorithms have been selected to find a model that best solves the classification problem provided by the training data:
- **AdaBoost**: Its ability to boost additional configurations of the features provided make it a likely candidate to predict match winners.
- **Random Forest**: Bagging a number of estimators with varying weights for each of our features can allow to make a well-revised prediction.
- **k-Nearest Neighbor**: The model can potentially detect similar characteristics from neighbouring games with similar statistical outcomes.
- **Neural Network**: Can iterate through the training models to identify additional characteristics and patterns in the features.
- **Logistic Regression**: Simple and effective model to train to solve a binary classification problem.
- **Support Vector Machine**: Can provide a decision function that separates the data convincingly.

### Methodology

To have a homogeneous training and testing data set, about 5000 matches were sampled per competitive tier. This ensures the player skill is equally represented in the samples, and do not influence the results. 1/5 of the data was held out for testing the models at the end; the samples have been stratified to ensure the tier distribution is maintained. No penalty was required to solve any imbalanced data, since there was an almost equal amount of samples for each of the labels analyzed. This contributed to limit data-driven asym- metric costs.

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
