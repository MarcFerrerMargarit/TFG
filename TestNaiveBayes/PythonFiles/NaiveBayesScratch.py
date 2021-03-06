import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

np.set_printoptions(precision=6)


class MultinomialNB(object):
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        count_sample = X.shape[0]
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
        count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
        self.feature_log_prob_ = np.log(count / count.sum(axis=1)[np.newaxis].T)
        return self

    def predict_log_proba(self, X):
        return [(self.feature_log_prob_ * x).sum(axis=1) + self.class_log_prior_
                for x in X]

    def predict(self, X):
        return np.argmax(self.predict_log_proba(X), axis=1)

class BernoulliNB(object):
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        count_sample = X.shape[0]
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
        count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
        smoothing = 2 * self.alpha
        n_doc = np.array([len(i) + smoothing for i in separated])
        self.feature_prob_ = count / n_doc[np.newaxis].T
        return self

    def predict_log_proba(self, X):
        return [(np.log(self.feature_prob_) * x + \
                 np.log(1 - self.feature_prob_) * np.abs(x - 1)
                ).sum(axis=1) + self.class_log_prior_ for x in X]

    def predict(self, X):
        return np.argmax(self.predict_log_proba(X), axis=1)


class GaussianNB(object):
    def __init__(self):
        pass

    def fit(self, X, y):
        print(X)
        for i in X:
            print(i[0])
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        # self.model = np.array([np.c_[np.mean(i, axis=0), np.std(i, axis=0)] for i in separated])
        return self

    def _prob(self, x, mean, std):
        exponent = np.exp(- ((x - mean)**2 / (2 * std**2)))
        return np.log(exponent / (np.sqrt(2 * np.pi) * std))

    def predict_log_proba(self, X):
        return [[sum(self._prob(i, *s) for s, i in zip(summaries, x))
                for summaries in self.model] for x in X]

    def predict(self, X):
        return np.argmax(self.predict_log_proba(X), axis=1)

    def score(self, X, y):
        return sum(self.predict(X) == y) / len(y)

def main():
    # iris = load_iris()
    # X, y = iris.data, iris.target
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25)
    # nb = GaussianNB().fit(X_train, y_train)
    # print("Gaussian Score Train: ", nb.score(X_train, y_train))
    # print("Gaussian Score Test: ", nb.score(X_test, y_test)

    #X = [[121, 80, 44], [180, 70, 43], [166, 60, 38], [153, 54, 37], [166, 65, 40], [190, 90, 47], [175, 64, 39],
         # [174, 71, 40], [159, 52, 37], [171, 76, 42], [183, 85, 43]]

    X = [[[121,133], 80, 44],
         [[180,140], 70, 43],
         [[166,180], 60, 38],
         [[153,170], 54, 37],
         [[166,160], 65, 40],
         [[190,180], 90, 47],
         [[175,170], 64, 39],
         [[174,173], 71, 40],
         [[159,160], 52, 37],
         [[171,150], 76, 42],
         [[183,133], 85, 43]
         ]

    Y = ['blanco', 'blanco', 'mediterraneo', 'mediterraneo', 'blanco', 'blanco', 'mediterraneo', 'mediterraneo',
         'mediterraneo', 'blanco', 'blanco']

    le = preprocessing.LabelEncoder()
    #le.fit(['blanco', 'mediterraneo'])
    le.fit(Y)
    labels = le.transform(Y)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=.25)
    nb = GaussianNB().fit(X_train, y_train)

    predict = nb.predict([[141, 78, 50]])
    print(le.inverse_transform(predict))


main()
