# Esports Prediction

## Abstract

League of Legends is a team-based strategy game requiring several skills to achieve victories. Predicting a winner from a given match can prove to be difficult, as several traits hold a level of importance to determining the victor. The study analyzes key parameters of a given match, such as overall statistics, objective first and game resources at a given time. From a set point in time, classification models (support vector machine, random forest and k-nearest neighbours to name a few) were trained against the most important features assessed using their correlation values. The prediction of a victor can be maximized to the point it surpasses a uniform random distribution; relying on parameters such that weights are properly distributed can further improve the model’s results.

---

## Introduction

League of Legends is a multiplayer online battle arena (MOBA) game where two teams of five players face off to destroy the other’s base. While the computerized sport possesses the luxury of providing instantly measurable data, analysts may find it difficult to predict the outcome of a match, due to the number of parameters that can fluctuate from one game to another, along with multiple factors that may influence the results. Through this study, we aim to attempt at maximizing the likelihood of predicting the victory of one League of Legends team over another and observe how machine learning can solve the problem in providing a good assessment of a team’s strength based on the information it is provided throughout a match.

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

### Measure of Success

To benchmark each model’s performance, a dummy classifier was created to provide a baseline to match against each of the scores posted. Using a uniform distribution, the classifier chooses a winner randomly, akin to flipping a coin.

| Measure | Value |
| --- | ----------- |
| Accuracy | 50.4 |
| Precision | 50.4 |
| Recall | 51.5 |

For us to declare a model as successful, its accuracy scores (Accuracy, Precision, Recall) must surpass that of the Dummy classifier by 50%; hence surpassing a threshold of 75% across the board.

### Preprocessing

Prior to training, a preprocessing pipeline was established to clean the data. Labels were set to red and blue-won games, and each of their corresponding features were collapsed against each other in order to record to which team the advantage leans; a negative value represents an advantage to the blue side, and a positive value to the red side. 

Two variants of the data were produced: The binary model only reports each advantage under two labels, while the difference variant keeps the integer value of that advantage. The latter retains some information regarding the intensity of the advantage a team might have against the other; A team with an advantage of thousands of gold may be decided earlier than a match where only 10 gold separates each team’s economy. 

Finally, a min-max scaling was perfomed on the data to simplify its visualization when cross-comparing features against each other; a value under 0.5 would lean towards a blue side victory, while values above 0.5 would give reason to the red side.

### Training

For each of the models selected, a number of hyperparameters were manipulated in order to find the best estimator for classifying the samples. To find the right set of hyperparameters, a cross-validation search was performed for the various properties held by the models. The lack of a data imbalance also avoids a large misclassification of data points belonging to a small class, which would require us to introduce penalties to a class handicapped by a lack of example. 

Two of the dimensions, kill and gold advantage, were used to plot and visualize the final trained models to provide a heuristic on the strategy each model is expecting to take. 

The figure below illustrates prediction map for kNN model, using two dimensions (kill advantage vs gold advantage)

<p alt="kNN" align="center"><a href="https://github.com/rmanaem/esports-prediction/blob/master/figures/plotting_knn.png"><img src="https://github.com/rmanaem/esports-prediction/blob/master/figures/plotting_knn.png?raw=true"/></a></p>

|  | Dummy | kNN | Random Forest | AdaBoost | Logistic Regression | SVM | Neural Network |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Accuracy | 50.4 | 90.35 | 90.48 | 90.12 | 90.28 | 90.40 | 90.22 |
| Precision | 50.4 | 89.61 | 89.71 | 89.40 | 89.87 | 89.70 | 89.35 |
| Recall | 51.5 | 91.26 | 91.41 | 91.00 | 90.75 | 91.26 | 91.31 |
| F1 Score | 50.94 | 90.43 | 90.55 | 90.31 | 90.36 | 90.48 | 90.32 |

The support vector machine took the longest to train. As
for random forest, it had the best fit against the training data.

<p alt="rf-confusion-matrix" align="center"><a href="https://github.com/rmanaem/esports-prediction/blob/master/figures/rf_confusion_matrix.png"><img src="https://github.com/rmanaem/esports-prediction/blob/master/figures/rf_confusion_matrix.png?raw=true"/></a></p>

The figure above illustrates the Random Forest’s confusion matrix against the training set.

Results posted by the neural network algorithm were not convincing enough to analyze the features provided. Across a total of 144 fits, the model capped at its local minima of
0.38. If added dimensions can provide more information to the model, it may be possible to train a model that can minimize the loss value against the dataset provided.

---

## Conclusion

### Observations

Compared to the dummy application, all models were able to surpass the threshold initially set prior to the study. Of the models trained, the k-nearest neighbours posted the strongest results. Its ability to rely on surrounding data points to assess a game’s victory makes it a proper fit for the game’s characteristics.

A team with a gold advantage and kill advantage increases its chance of winning a game convincingly. While this may seem to be an evident observation, it is worthwhile to highlight that gold advantage ranked higher than kills during feature analysis. With this insight, it follows that a team may find more worth in collecting resources increasing their economy over seeking fights putting their winning chances at risk.

On the other end, resources such as rift and plates give
an early advantage, but lose value over time; investing in
them may not be the most optimal choice if they are faced to longer standing ones, like creep score or towers.

The table below shows samples misclassified as blue victories (random forest estimator). Negative values are advantages to the blue team, positive values to the red team. Columns for inhibitor and baron specify the team that obtained the first one, while the remaining four represent the size of difference.

| inhibitor | baron | kills | gold | damage | towers |
| :---: | :---: | :---: | :---: | :---: | :---: |
| blue | red | 4 | -2391 | -15982 | -5 |
| blue | red | 6 | -1637 | -3938 | -1 |
| blue | blue | 7 | 5682 | 15075 | 3 |
| blue | red | 5 | 1811 | 13800 | 1 |
| blue | blue | -15 | -1472 | -12730 | -4 |
| blue | red | 0 | -5792 | -16715 | -2 |

When verifying the misclassified samples, we can identify the bias the model had in response to the first team holding the inhibitor. This can lead to a loss of precision by the model, which can be observed by the smaller precision scores posted by all models. While first objectives are good indicators to a team’s capacity to win, it may be important to weight them such that it does not affect precision scores negatively, as shown above.

### Improvements

Our models limited themselves to analyzing a single frame. It is possible, however, to feed the model with a time series, and have it predict the full outcome of the game on a minute-to-minute basis. It may be required to pre-process a uniform data set with an equal amount of frames for each sample. Feeding the data to a Neural Network can seek at finding patterns related to the flow of an ongoing game.

To conclude, other data sources prove helpful to learn additional features. Leaguepedia API, an open-source wiki, keeps a record of every LoL player statistics in a season, which can be factored in to approximate the strength of each player participating in a match. The champion’s strength can also be a relevant indicator to configure using the Lolesports API, another Riot hosted data source saving the order of items purchased by the user.

---

## Setup

Install the dependencies outlined in the requirements.txt file. For convenience, you can use Python's `venv` package to install dependencies in a virtual environment. You can find the instructions on creating and activating a virtual environment in the official [documentation](https://docs.python.org/3.10/library/venv.html). After setting up and activating your environment, you can install the dependencies by running the following command in your terminal:

```bash
$ pip install -r requirements.txt
```

**Note**: a Riot API key is also needed for the API Client to work, which you can get here: <https://developer.riotgames.com/>

Follow these steps:

1. Fetch the game ids with the following command

```bash
python src/fetch_game_ids.py
```

2. Extract the game data using the following command **(Note: this step may take very long (ETA:20 hours)**

```bash
python src/extract_game_data.py
```

3. Run the `processing.ipynb` to pre-process the data prior to analysis

4. Use the `training.ipynb` file to train the machine learning models