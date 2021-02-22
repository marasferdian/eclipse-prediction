import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

RSEED = 50

df = pd.read_csv('./solar-eclipses-NN.csv').sample(55000, random_state=RSEED)
#df['Date'] = pd.to_datetime(df['Date'])
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

# Train tree
tree = DecisionTreeClassifier(random_state=RSEED, max_depth=25)
tree.fit(train, train_labels)
print(f'Decision tree has {tree.tree_.node_count} nodes with maximum depth {tree.tree_.max_depth}.')
print(f'Model Accuracy: {tree.score(train, train_labels)}')
# we get 1.0 accuracy (100%); is it overfitted?

# wrong_test_labels = []
# for each in test_labels:
#     if each == 1:
#         wrong_test_labels.append(0)
#     else:
#         wrong_test_labels.append(1)

print(f'Test Accuracy: {tree.score(test, test_labels)}')
print(99.19393939393939 / 100 * len(test))
print("correct out of")
print(len(test))

predictions = tree.predict(test)
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

