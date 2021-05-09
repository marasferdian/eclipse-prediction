import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from ML.confusion_matrix_helper import make_confusion_matrix
from sklearn.metrics import f1_score, recall_score, precision_score

RSEED = 50


df = pd.read_csv('lunar-eclipses-classif.csv')
#df = pd.read_csv('./solar-eclipses-classif.csv')
df['Is Eclipse'] = df['Is Eclipse'].replace({True: 1, False: 0})
print(df.head())
labels = np.array(df['Is Eclipse'])
train = df[:int(0.4636 * len(df))]
train_labels = np.array(train.pop('Is Eclipse'))
print(train.head())
neg = 0
pos = 0
counter = 0
print(neg, pos)
print(df.shape)

final_test_df = df[int(0.4636 * len(df)):]
print(final_test_df.head())
final_test_labels = np.array(final_test_df.pop('Is Eclipse'))
df.set_index('Date', inplace=True)
final_test_df.set_index('Date', inplace=True)
train.set_index('Date', inplace=True)
#train_dates = train.pop('Date')
df = df.select_dtypes('number')
final_test_df = final_test_df.select_dtypes('number')
train = train.select_dtypes('number')

features = list(train.columns)

knn = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=None, n_neighbors=7, p=2, weights='uniform')
knn.fit(train, train_labels)
print(f'Model Accuracy: {knn.score(train, train_labels)}')

print(f'Test Accuracy: {knn.score(final_test_df, final_test_labels)}')
print(knn.score(final_test_df, final_test_labels) * len(final_test_df))
print("correct out of")
print(len(final_test_df))
predictions = knn.predict(final_test_df)
wrong = 0
eclipses = 0
false_positives = 0
for i in range(len(final_test_labels)):
    if final_test_labels[i] == 1 and predictions[i] == 1:
        eclipses += 1
    if predictions[i] != final_test_labels[i]:
        if predictions[i] == 1:
            false_positives += 1
        print(str(final_test_df.index[i]) + " was marked as " + str(predictions[i]) +" but is actually " + str(final_test_labels[i]))
        wrong += 1

print(eclipses)

actual = 0
for each in final_test_labels:
    if each == 1:
        actual += 1

print("predicted out of")
print(actual)

print("Final accuracy:")
accuracy = (eclipses - false_positives) / actual

print(accuracy)
print("Recall")
print(recall_score(final_test_labels, predictions))
print("Precision")
print(precision_score(final_test_labels, predictions))
print("F1")
f1 = f1_score(final_test_labels, predictions)
print(f1)
labels = ['True Negatives','False Positives','False Negatives','True Positives']
categories = ['Zero', 'One']
cf_matrix = confusion_matrix(final_test_labels, predictions)
make_confusion_matrix(cf_matrix,
                      accuracy=accuracy,
                      f1=f1,
                      group_names=labels,
                      categories=categories,
                      cbar=False,
                      title='k-Nearest Neighbors (k=7)')
