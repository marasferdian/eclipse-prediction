import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

RSEED = 50

df = pd.read_csv('./solar-eclipses-NN.csv').sample(55000, random_state=RSEED)
df.set_index('Date', inplace=True)
df['Is Eclipse'] = df['Is Eclipse'].replace({True: 1, False: 0})
df = df.select_dtypes('number')
print(df.head())
labels = np.array(df.pop('Is Eclipse'))
train, test, train_labels, test_labels = train_test_split(df, labels,
                                                          stratify=labels,
                                                          test_size=0.3,
                                                          random_state=RSEED)
features = list(train.columns)
print(train.shape)
print(test.shape)

knn = KNeighborsClassifier(n_neighbors=1)
# best accuracy for n = 1
knn.fit(train, train_labels)
print(f'Model Accuracy: {knn.score(train, train_labels)}')

print(f'Test Accuracy: {knn.score(test, test_labels)}')
print(99.41212121212121 / 100 * len(test))
print("correct out of")
print(len(test))
predictions = knn.predict(test)
wrong = 0
eclipses = 0
for i in range(len(test_labels)):
    if test_labels[i] == 1 and predictions[i] == 1:
        eclipses += 1
    if predictions[i] != test_labels[i]:
        print(test.index[i] + " was marked as " + str(predictions[i]) +" but is actually " + str(test_labels[i]))
        wrong += 1

print(eclipses)

actual = 0
for each in test_labels:
    if each == 1:
        actual += 1

print("predicted out of")
print(actual)

