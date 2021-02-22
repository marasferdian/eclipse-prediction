from math import sqrt
from threading import Thread

import ephem
import pandas as pd
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime, date, timedelta
from helper_functions import get_sun_moon_angular_radius, get_separation, check_if_any_coord_validate_eq, \
    is_initial_separation_condition_valid


def compute_abs_diff(moon_alt, moon_az, sun_alt, sun_az, debug=False):
    alt_diff = abs(moon_alt - sun_alt)
    az_diff = abs(moon_az - sun_az)
    if debug:
        print("Alt diff: " + str(alt_diff))
        print("Az diff: " + str(az_diff))
        print("Sum: " + str(alt_diff + az_diff))
    return sqrt(alt_diff ** 2 + az_diff ** 2)


def compute_sun_moon_positions(date, debug=False):
    # print("Date: " + date)
    obs = ephem.Observer()
    obs.lon = '0'
    obs.lat = '0'
    obs.elevation = 0
    obs.date = date
    moon_pos = ephem.Moon(obs)

    date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    time = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)
    sun_pos = sunpos(time, 0, 0, 0)
    moon_pos_alt = str(moon_pos.alt).split(":")
    moon_pos_alt_deg = float(moon_pos_alt[0])
    moon_pos_alt_min = float(moon_pos_alt[1])
    moon_pos_alt_sec = float(moon_pos_alt[2])
    moon_pos_alt_zec = moon_pos_alt_deg + moon_pos_alt_min / 60 + moon_pos_alt_sec / 3600
    moon_pos_az = str(moon_pos.az).split(":")
    moon_pos_az_deg = float(moon_pos_az[0])
    moon_pos_az_min = float(moon_pos_az[1])
    moon_pos_az_sec = float(moon_pos_az[2])
    moon_pos_az_zec = moon_pos_az_deg + moon_pos_az_min / 60 + moon_pos_az_sec / 3600
    # print("Moon position: (" + str(moon_pos_alt_zec) + " , " + str(moon_pos_az_zec) + ")")
    # print("Sun position: " + str(sun_pos))
    err = compute_abs_diff(moon_pos_alt_zec, moon_pos_az_zec, sun_pos[0], sun_pos[1], debug)
    if debug:
        print("\n")
    return err


def get_closest_hour_positions(date_str: str, debug=False):
    best = '', 100000.0
    hours = [(str(x) + y) for x in range(24) for y in [':00:00']]
    for h in hours:
        pos = compute_sun_moon_positions(date_str + ' ' + h)
        if pos < best[1]:
            best = h, pos
    if debug:
        print('Closest value for ' + date_str + ': ' + str(best[1]) + ' at ' + best[0])
    return best


def get_closest_hour_separation(date_str: str):
    found = False
    best_val = - 10000
    best_coordinates = ''
    best_h = -1
    hours = [(str(x) + y) for x in range(24) for y in [':00:00', ':20:00', ':40:00']]
    for h in hours:
        bool, best, best_coord = check_if_any_coord_validate_eq(date_str + ' ' + h)
        if bool:
            found = True
            if best > best_val:
                best_val = best
                best_coordinates = best_coord
                best_h = h
    return found, best_h, best_coordinates


df = pd.read_csv('./solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(200)

eclipses_list = df['Date'].tolist()
eclipse_actual_time = df['GrEclTime'].tolist()


def get_eclipses_using_closest_hour():
    correct = 0
    missed = 0
    false_positives = 0
    start_date = date(2012, 1, 1)
    end_date = date(2100, 12, 31)
    delta = timedelta(days=1)
    while start_date <= end_date:
        date_str = datetime.strftime(start_date, '%Y-%m-%d')
        best = get_closest_hour_positions(date_str, False)
        sun_rad, moon_rad = get_sun_moon_angular_radius(date_str)
        coeff = 2.7
        err = (sun_rad + moon_rad) * coeff
        if best[1] < err:
            if date_str in eclipses_list:
                correct += 1
            else:
                false_positives += 1
        else:
            if date_str in eclipses_list:
                missed += 1
        start_date += delta

    print("Correct:" + str(correct))
    print("Missed: " + str(missed))
    print("False positives: " + str(false_positives))


def get_all_eclipses(start_date, end_date, get_all_locations=False):
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


class GetEclipsesThread(Thread):
    def __init__(self, start_date, end_date, output_list: list, get_all_locations):
        super().__init__()
        self.get_all_locations = get_all_locations
        self.start_date = start_date
        self.end_date = end_date
        self.output_list = output_list

    def run(self) -> None:
        self.output_list.extend(get_all_eclipses(self.start_date, self.end_date, self.get_all_locations))


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


def print_values():
    for eclipse, time in zip(eclipses_list, eclipse_actual_time):
        print("Eclipse date: " + str(eclipse) + ' ' + str(time))
        sun_rad, moon_rad = get_sun_moon_angular_radius(eclipse + ' ' + time)
        print("Sun rad: " + str(sun_rad))
        print("Moon rad: " + str(moon_rad))
        sep = get_separation(eclipse + ' ' + time)
        print("Separation: " + str(sep))
        print("\n")




# get_eclipses_using_closest_hour()
get_all_ecl_2020_2100(get_all_locations=True)
