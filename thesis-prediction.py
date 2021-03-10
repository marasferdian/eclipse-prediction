import pandas as pd
import matplotlib.pyplot as plt
from pandas import datetime
from statsmodels.tsa.arima.model import ARIMA
import datetime as dt
from statsmodels.tsa.stattools import adfuller

df = pd.read_csv('./solar-eclipses.csv', parse_dates=['Date'])
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


# the initial version
def get_future_eclipses_v0(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    date = new_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 5
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


# with optimization for asc/desc nodes - BEST YET!!!
def get_future_eclipses_v1(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    mean_offsets = get_nodes_mean_offset(asc_node, desc_node)
    asc_mean_offset = mean_offsets[0]
    desc_mean_offset = mean_offsets[1]
    asc_node += dt.timedelta(days=asc_mean_offset)
    desc_node += dt.timedelta(days=desc_mean_offset)
    date = new_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.235
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


# gets asc/desc nodes from df (uses real, not predicted values) + optimization for synodic month
def get_future_eclipses_v2(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    end_date = datetime.strptime('2040-05-11', '%Y-%m-%d')
    date = new_moon + dt.timedelta(hours=get_synodic_mean_offset(new_moon))
    ans = []
    # try not to hardcode this....get index by value for asc and desc nodes
    initial_index = 171
    i = 0
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.3
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node = datetime.strptime(asc_nodes[initial_index + i], '%Y-%m-%d %H:%M')
        desc_node = datetime.strptime(desc_nodes[initial_index + i], '%Y-%m-%d %H:%M')
        date += synodic_month
        i += 1

    return ans


# offset for asc/desc nodes + synodic month
def get_future_eclipses_v3(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    mean_offsets = get_nodes_mean_offset(asc_node, desc_node)
    asc_mean_offset = mean_offsets[0]
    desc_mean_offset = mean_offsets[1]
    synodic_month_offset = get_synodic_mean_offset(new_moon)
    new_moon += dt.timedelta(hours=synodic_month_offset)
    asc_node += dt.timedelta(days=asc_mean_offset)
    desc_node += dt.timedelta(days=desc_mean_offset)
    date = new_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.18655
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


# only synodic month offset added
def get_future_eclipses_v4(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    synodic_month_offset = get_synodic_mean_offset(new_moon)
    new_moon += dt.timedelta(hours=synodic_month_offset)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    date = new_moon
    ans = []
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.238
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

        date += synodic_month

    return ans


def get_future_eclipses_v6(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    synodic_month = dt.timedelta(days=29.530587981)
    end_date = datetime.strptime('2100-12-31', '%Y-%m-%d')
    ans = []
    initial_index = 158
    for i in range(initial_index, len(new_moon_dates)):
        date = datetime.strptime(new_moon_dates[i], '%Y-%m-%d %H:%M')
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.32
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node += dt.timedelta(days=draconic_month)
        desc_node += dt.timedelta(days=draconic_month)

    return ans

# get both new moon and nodes (real values)
def get_future_eclipses_v7(new_moon, asc_node, desc_node):
    draconic_month = 27.212220
    end_date = datetime.strptime('2040-05-11', '%Y-%m-%d')
    ans = []
    initial_id_synodic = 158
    initial_id_node = 171
    i = 0
    date = new_moon
    while date < end_date:
        asc_node_dif = abs(date - asc_node).days % draconic_month
        desc_node_dif = abs(date - desc_node).days % draconic_month
        asc_node_dif = min(asc_node_dif, draconic_month - asc_node_dif)
        desc_node_dif = min(desc_node_dif, draconic_month - desc_node_dif)
        error = 1.3
        print(date, min(asc_node_dif, desc_node_dif))
        if min(asc_node_dif, desc_node_dif) < error:
            ans.append(date)
        asc_node = datetime.strptime(asc_nodes[initial_id_node + i], '%Y-%m-%d %H:%M')
        desc_node = datetime.strptime(desc_nodes[initial_id_node + i], '%Y-%m-%d %H:%M')
        date = datetime.strptime(new_moon_dates[initial_id_synodic + i], '%Y-%m-%d %H:%M')
        i += 1

    return ans


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


def print_predictions_v1():
    reference_date = datetime.strptime('2013-11-03 12:47:36', '%Y-%m-%d %H:%M:%S')
    asc_node = datetime.strptime('2013-10-06 22:08:00', '%Y-%m-%d %H:%M:%S')
    desc_node = datetime.strptime('2013-10-19 21:47:00', '%Y-%m-%d %H:%M:%S')
    eclipses = get_future_eclipses_v0(reference_date, asc_node, desc_node)
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


def print_predictions_v2():
    reference_date = datetime.strptime('2013-11-03 12:47:36', '%Y-%m-%d %H:%M:%S')
    asc_node = datetime.strptime('2013-10-06 22:08:00', '%Y-%m-%d %H:%M:%S')
    desc_node = datetime.strptime('2013-10-19 21:47:00', '%Y-%m-%d %H:%M:%S')
    eclipses = get_future_eclipses_v7(reference_date, asc_node, desc_node)
    count_correct = 0
    for d in eclipses:
        flag = 'OK' if check_if_prediction_is_correct(d) else 'NOT OK'
        print(datetime.strftime(d, '%Y-%m-%d %H:%M:%S') + ' ' + flag)
        if flag == 'OK':
            count_correct += 1
    print('Total found: ' + str(len(eclipses)))
    print('Correct: ' + str(count_correct))
    print('False positives: ' + str(len(eclipses) - count_correct))
    print('Missed: ' + str(60 - count_correct))
    print('Accuracy: ' + str(count_correct * 100 / 60) + ' %')


#print_predictions_v2()
print_predictions_v1()
