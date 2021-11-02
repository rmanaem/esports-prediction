import csv
import sklearn
import sklearn.model_selection 
import sklearn.tree
import sklearn.ensemble
import sklearn.preprocessing
import sklearn.metrics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 200 years
RANDOM_STATE = 200
def main():
    with open('lol-results-final.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        games = [tuple(row) for row in reader if tuple(row)[8] != '']
    X = np.array([g[9:] for g in games], dtype=np.int32)
    y = np.array([0 if g[8] == g[6] else 1 for g in games])

    def combine(x):
        # print(x)
        x_i = x.reshape(2,7)
        return x_i[0,:] - x_i[1,:]

    X = np.apply_along_axis(combine, 1, X)

    # Splitting
    X_train, X_int, y_train, y_int = sklearn.model_selection.train_test_split(X, y, test_size=0.4,random_state=RANDOM_STATE)
    X_test, X_val, y_test, y_val = sklearn.model_selection.train_test_split(X_int, y_int, test_size=0.5, random_state=RANDOM_STATE)
    scaler = sklearn.preprocessing.MinMaxScaler()
    scaler.fit(X_train)
    X_train_scl = scaler.transform(X_train)
    X_test_scl = scaler.transform(X_test)
    X_val_scl = scaler.transform(X_val)


    # Training
    clf = sklearn.ensemble.RandomForestClassifier(n_estimators=10, random_state=RANDOM_STATE).fit(X_train_scl,y_train)

    # sklearn.tree.plot_tree(clf)
    # plt.show()

    # Testing
    y_pred_val = clf.predict(X_val)
    print(sklearn.metrics.accuracy_score(y_val, y_pred_val))

    y_pred_test = clf.predict(X_test)
    print(sklearn.metrics.accuracy_score(y_val, y_pred_test))
    # print(X[:5], X.shape)
    # datum = X[0].reshape(2,7)
    # print(datum[0,:] - datum[1,:])

if __name__ == '__main__':
    main()