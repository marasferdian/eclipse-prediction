import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.ensemble import RandomForestClassifier

from ML.confusion_matrix_helper import make_confusion_matrix

RSEED = 50

df = pd.read_csv('lunar-eclipses-classif.csv')
df['Is Eclipse'] = df['Is Eclipse'].replace({True: 1, False: 0})
labels = np.array(df['Is Eclipse'])
train = df[:int(0.4636 * len(df))]
train_labels = np.array(train.pop('Is Eclipse'))

print(train.head())
neg = 0
pos = 0
counter = 0

final_test_df = df[int(0.4636 * len(df)):]
print(final_test_df.head())
final_test_labels = np.array(final_test_df.pop('Is Eclipse'))
df.set_index('Date', inplace=True)
final_test_df.set_index('Date', inplace=True)
train.set_index('Date', inplace=True)
df = df.select_dtypes('number')
final_test_df = final_test_df.select_dtypes('number')
train = train.select_dtypes('number')

features = list(train.columns)
print(train.shape)
# tree = DecisionTreeClassifier(random_state=RSEED, max_depth=2)
tree = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=2, min_samples_split=30, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None)
tree.fit(train, train_labels)
#print(f'Decision tree has {tree.tree_.node_count} nodes with maximum depth {tree.tree_.max_depth}.')
print(f'Model Accuracy: {tree.score(train, train_labels)}')
print(f'Test Accuracy: {tree.score(final_test_df, final_test_labels)}')
print(tree.score(final_test_df, final_test_labels) * len(final_test_df))
print("correct out of")
print(len(final_test_df))
predictions = tree.predict(final_test_df)
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
labels = ['True Negatives','False Positives','False Negatives','True Positives']
categories = ['Zero', 'One']
cf_matrix = confusion_matrix(final_test_labels, predictions)
f1 = f1_score(final_test_labels, predictions)
make_confusion_matrix(cf_matrix,
                      accuracy=accuracy,
                      f1=f1,
                      group_names=labels,
                      categories=categories,
                      cbar=False,
                      title='Random Forest (max depth=2)')

