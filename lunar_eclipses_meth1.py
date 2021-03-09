import pandas as pd
import matplotlib.pyplot as plt
from pandas import datetime
from statsmodels.tsa.arima.model import ARIMA
import datetime as dt

df = pd.read_csv('./lunar-eclipses.csv', parse_dates=['Date'])
df = df.tail(200)

list = df['Date'].tolist()
time = df['GrEclTime'].tolist()
dates_and_times = [datetime.strptime(d + ' ' + t, '%Y-%m-%d %H:%M:%S') for d, t in zip(list, time)]
date_format = '%Y-%m-%d'

nodes_df = pd.read_csv('./moon-passage-v2.csv')
asc_nodes = nodes_df['Ascending']
desc_nodes = nodes_df['Descending']

synodic_months_df = pd.read_csv('./synodic-month-lengths.csv')
new_moon_dates = synodic_months_df['Date']

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


def get_nodes_mean_offset(asc_node, desc_node):
    draconic_month = 27.212220
    offset_asc_node = 0
    offset_desc_node = 0
    predicted_next_asc = asc_node
    predicted_next_desc = desc_node
    initial_index = 171
    iterations = 0
    for i in range(initial_index, len(nodes_df)):
        real_asc_node = datetime.strptime(asc_nodes[i], '%Y-%m-%d %H:%M')
        real_desc_node = datetime.strptime(desc_nodes[i], '%Y-%m-%d %H:%M')
        offset_asc_node += (real_asc_node - predicted_next_asc).days
        offset_desc_node += (real_desc_node - predicted_next_desc).days
        predicted_next_asc += dt.timedelta(days=draconic_month)
        predicted_next_desc += dt.timedelta(days=draconic_month)
        iterations += 1

    mean_asc_node_diff = offset_asc_node / iterations
    mean_desc_node_diff = offset_desc_node / iterations
    return mean_asc_node_diff, mean_desc_node_diff


def get_synodic_mean_offset(date):
    synodic_month = dt.timedelta(days=29.530587981)
    # again, TRY not to hardcode this
    initial_index = 158
    offset = 0
    predicted_new_moon = date
    iterations = 0
    for i in range(initial_index, len(new_moon_dates)):
        real_new_moon = datetime.strptime(new_moon_dates[i], '%Y-%m-%d %H:%M')
        offset += (real_new_moon - predicted_new_moon).seconds / 3600
        predicted_new_moon += synodic_month
        iterations += 1

    mean_offset = offset / iterations
    return mean_offset


# the initial version
def get_future_eclipses_v0(full_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.53059)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    date = full_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.17
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


def get_future_eclipses_v1(full_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.53059)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    mean_offsets = get_nodes_mean_offset(asc_node, desc_node)
    asc_mean_offset = mean_offsets[0]
    desc_mean_offset = mean_offsets[1]
    asc_node += dt.timedelta(days=asc_mean_offset)
    desc_node += dt.timedelta(days=desc_mean_offset)

    date = full_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.17
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


def check_if_prediction_is_correct(date):
    error = 1.6
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


def print_predictions_v1():
    reference_date = datetime.strptime('2013-12-17 11:29:00', '%Y-%m-%d %H:%M:%S')
    asc_node = datetime.strptime('2013-10-06 22:08:00', '%Y-%m-%d %H:%M:%S')
    desc_node = datetime.strptime('2013-10-19 21:47:00', '%Y-%m-%d %H:%M:%S')
    eclipses = get_future_eclipses_v1(reference_date, asc_node, desc_node)
    count_correct = 0
    for d in eclipses:
        flag = 'OK' if check_if_prediction_is_correct(d) else 'NOT OK'
        print(datetime.strftime(d, '%Y-%m-%d %H:%M:%S') + ' ' + flag)
        if flag == 'OK':
            count_correct += 1
    print('Total found: ' + str(len(eclipses)))
    print('Correct: ' + str(count_correct))
    print('False positives: ' + str(len(eclipses) - count_correct))
    print('Missed: ' + str(197 - count_correct))
    print('Accuracy: ' + str(count_correct * 100 / 197) + ' %')


print_predictions_v1()
