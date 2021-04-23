import pandas as pd
from pandas import datetime
import datetime as dt
import numpy as np

from ML.confusion_matrix_helper import make_confusion_matrix

df = pd.read_csv('solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(200)

list = df['Date'].tolist()
time = df['GrEclTime'].tolist()
dates_and_times = [datetime.strptime(d + ' ' + t, '%Y-%m-%d %H:%M:%S') for d, t in zip(list, time)]
date_format = '%Y-%m-%d'

synodic_month = dt.timedelta(days=29.53059)
draconic_month = 27.21222


def calculate_avg_error(predicted, expected):
    err = 0
    for i in range(len(predicted)):
        err += abs(predicted[i] - expected[i])
    err = err / len(predicted)
    return err


def get_orbit_position(period, reference, current):
    dif = (current - reference).days
    q = dif // period
    return dif - period * q


def get_future_eclipses(new_moon, asc_node, desc_node):
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    date = new_moon
    ans = []
    total_tries = (end_date - date).days
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.25
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans, total_tries


def check_if_prediction_is_correct(date):
    error = 1.5
    l = 0
    r = len(dates_and_times) - 1
    while l <= r:
        m = (l + r) // 2
        if dates_and_times[m] >= date - dt.timedelta(days=error):
            r = m - 1
        else:
            l = m + 1
    if l == len(dates_and_times):
        return False
    return abs((date - dates_and_times[l]).days) <= error



def print_predictions():
    reference_date = datetime.strptime('2020-06-21 06:41:15', '%Y-%m-%d %H:%M:%S')  # an eclipse
    asc_node = datetime.strptime('2020-06-21 04:24:00', '%Y-%m-%d %H:%M:%S')
    desc_node = datetime.strptime('2020-06-06 18:10:00', '%Y-%m-%d %H:%M:%S')
    eclipses, total_tries = get_future_eclipses(reference_date, asc_node, desc_node)
    count_correct = 0
    for d in eclipses:
        flag = 'OK' if check_if_prediction_is_correct(d) else 'NOT OK'
        # print(datetime.strftime(d, '%Y-%m-%d %H:%M:%S') + ' ' + flag)
        if flag == 'OK':
            count_correct += 1
    print('Total found: ' + str(len(eclipses)))
    print('Correct: ' + str(count_correct))
    print('False positives: ' + str(len(eclipses) - count_correct))
    print('Missed: ' + str(182 - count_correct))
    acc = (count_correct - (len(eclipses) - count_correct)) / 182
    print('Accuracy: ' + str(acc))

    TN = total_tries - 182 - len(eclipses) - count_correct
    FP = len(eclipses) - count_correct
    FN = 182 - count_correct
    TP = count_correct
    acc = (count_correct - (len(eclipses) - count_correct)) / 182
    recall = count_correct / 182
    precision = count_correct / (count_correct + (len(eclipses) - count_correct))
    f1 = 2 * (precision * recall) / (precision + recall)
    labels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']
    categories = ['Zero', 'One']
    cf_matrix = np.array([[TN, FP], [FN, TP]])
    make_confusion_matrix(cf_matrix,
                          accuracy=acc,
                          f1=f1,
                          group_names=labels,
                          categories=categories,
                          cbar=False,
                          title='Solar Eclipses')


print_predictions()