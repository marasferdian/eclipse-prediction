import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score

from ML.confusion_matrix_helper import make_confusion_matrix

df = pd.read_csv('lunar-eclipses-classif.csv')
df['Is Eclipse'] = df['Is Eclipse'].replace({True: 1, False: 0})
labels = np.array(df['Is Eclipse'])
train = df[:int(0.4636 * len(df))]
train_labels = np.array(train.pop('Is Eclipse'))
print(train)
test = df[int(0.4636 * len(df)):]
test_labels = np.array(test.pop('Is Eclipse'))
df.set_index('Date', inplace=True)
test.set_index('Date', inplace=True)
train.set_index('Date', inplace=True)
df = df.select_dtypes('number')
test = test.select_dtypes('number')
train = train.select_dtypes('number')


features = list(train.columns)

logisticRegr = LogisticRegression(verbose=True)
logisticRegr.fit(train, train_labels)
print(logisticRegr.predict_proba(test))
predictions = logisticRegr.predict(test)
wrong = 0
eclipses = 0
false_positives = 0
for i in range(len(test_labels)):
    if test_labels[i] == 1 and predictions[i] == 1:
        eclipses += 1
    if predictions[i] != test_labels[i]:
        if predictions[i] == 1:
            false_positives += 1
        print(str(test.index[i]) + " was marked as " + str(predictions[i]) + " but is actually " + str(test_labels[i]))
        wrong += 1

print(eclipses)

actual = 0
for each in test_labels:
    if each == 1:
        actual += 1

print("predicted out of")
print(actual)

print("Final accuracy:")
print((eclipses - false_positives) / actual)

accuracy = (eclipses - false_positives) / actual
labels = ['True Negatives','False Positives','False Negatives','True Positives']
categories = ['Zero', 'One']
cf_matrix = confusion_matrix(test_labels, predictions)
f1 = f1_score(test_labels, predictions)
make_confusion_matrix(cf_matrix,
                      accuracy=accuracy,
                      f1=f1,
                      group_names=labels,
                      categories=categories,
                      cbar=False,
                      title='Logistic Regression')
