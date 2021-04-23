from threading import Thread

import pandas as pd
from datetime import datetime, date, timedelta
from numerical_methods.helper_functions import *


def get_closest_hour_separation(date_str: str):
    found = False
    best_val = - 10000
    best_coordinates = ''
    best_h = -1
    hours = [(str(x) + y) for x in range(24) for y in [':00:00']]
    for h in hours:
        bool, best, best_coord = check_if_any_coord_validate_eq(date_str + ' ' + h)
        if bool:
            found = True
            if best > best_val:
                best_val = best
                best_coordinates = best_coord
                best_h = h
    return found, best_h, best_coordinates


def get_closest_hour_separation_lunar(date_str: str):
    found = False
    best_val = 10000
    best_coordinates = ''
    best_h = -1
    # hours = [(str(x) + y) for x in range(24) for y in [':00:00', ':20:00', ':40:00']]
    hours = [(str(x) + y) for x in range(24) for y in [':00:00']]
    for h in hours:
        bool, best, best_coord = check_if_any_coord_validate_eq_lunar(date_str + ' ' + h)
        if bool:
            found = True
            if best < best_val:
                best_val = best
                best_coordinates = best_coord
                best_h = h
    return found, best_h, best_coordinates


def get_all_solar_eclipses(start_date, end_date, get_all_locations=False):
    best = ''
    best_coord = ''
    eclipses = []
    delta = timedelta(days=1)
    while start_date < end_date:
        date_str = datetime.strftime(start_date, '%Y-%m-%d')
        # print("Calculating for " + date_str)
        if is_initial_separation_condition_valid(date_str):
            is_eclipse, best, best_coord = get_closest_hour_separation(date_str)
        else:
            is_eclipse = False
        if is_eclipse:
            eclipses.append(date_str)
            print("For date " + date_str + " there will be an eclipse visible at " + str(best) + "at coordinates ("
                                                                                                 "long:lat) " +
                  best_coord)
            if get_all_locations:
                start_date += delta
            else:
                start_date += timedelta(days=20)
        else:
            start_date += delta

    return eclipses


def get_all_lunar_eclipses(start_date, end_date, get_all_locations=False):
    best = ''
    best_coord = ''
    eclipses = []
    delta = timedelta(days=1)
    while start_date < end_date:
        date_str = datetime.strftime(start_date, '%Y-%m-%d')
        print("Calculating for " + date_str)
        is_eclipse, best, best_coord = get_closest_hour_separation_lunar(date_str)
        if is_eclipse:
            if date_str not in eclipses_list:
                print('!' + date_str)
            eclipses.append(date_str)
            print("For date " + date_str + " there will be an eclipse visible at " + str(best) + "at coordinates ("
                                                                                                 "long:lat) " +
                  best_coord)
            if get_all_locations:
                start_date += delta
            else:
                start_date += timedelta(days=20)
        else:
            start_date += delta

    print(eclipses)
    return eclipses


class GetEclipsesThread(Thread):
    def __init__(self, start_date, end_date, output_list: list, get_all_locations):
        super().__init__()
        self.get_all_locations = get_all_locations
        self.start_date = start_date
        self.end_date = end_date
        self.output_list = output_list

    def run(self) -> None:
        self.output_list.extend(get_all_solar_eclipses(self.start_date, self.end_date, self.get_all_locations))


def get_all_ecl_2020_2100(get_all_locations=False):
    ranges = [(x, x + 10) for x in range(2020, 2100, 10)]
    matches = []
    threads = []
    for r in ranges:
        m = []
        t = GetEclipsesThread(date(r[0], 1, 1), date(r[1], 1, 1), m, get_all_locations=get_all_locations)
        threads.append(t)
        matches.append(m)
        t.start()
    for t in threads:
        t.join()
    ans = []
    for m in matches:
        ans.extend(m)

    print(ans)
    return ans


df = pd.read_csv('solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(200)

eclipses_list = df['Date'].tolist()
eclipse_actual_time = df['GrEclTime'].tolist()
# get_all_ecl_2020_2100(get_all_locations=False)

get_all_solar_eclipses(date(2020, 1, 1), date(2100, 12, 31))
