from math import sqrt
import ephem
import pandas as pd
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime,date,timedelta

def compute_abs_diff(moon_alt, moon_az, sun_alt, sun_az, debug=False):
    alt_diff = abs(moon_alt - sun_alt)
    az_diff = abs(moon_az - sun_az)
    if debug:
        print("Alt diff: " + str(alt_diff))
        print("Az diff: " + str(az_diff))
        print("Sum: " + str(alt_diff + az_diff))
    return sqrt(alt_diff ** 2 + az_diff ** 2)


def compute_sun_moon_positions(date, debug=False):

    #print("Date: " + date)
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
    #print("Moon position: (" + str(moon_pos_alt_zec) + " , " + str(moon_pos_az_zec) + ")")
    #print("Sun position: " + str(sun_pos))
    err = compute_abs_diff(moon_pos_alt_zec, moon_pos_az_zec, sun_pos[0], sun_pos[1], debug)
    if debug:
        print("\n")
    return err


def get_closest_hour(date_str: str, debug=False):
    hours = [(str(x) + ':00:00') for x in range(24)]
    best = '', 100000.0
    for h in hours:
        pos = compute_sun_moon_positions(date_str + ' ' + h)
        if pos < best[1]:
            best = h, pos
    if debug:
        print('Closest value for ' + date_str + ': ' + str(best[1]) + ' at ' + best[0])
    return best


df = pd.read_csv('./solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(200)

eclipses_list = df['Date'].tolist()
eclipse_actual_time = df['GrEclTime'].tolist()
correct = 0
missed = 0
false_positives = 0
start_date = date(2012, 1, 1)
end_date = date(2100, 12, 31)
delta = timedelta(days=1)
while start_date <= end_date:
    date_str = datetime.strftime(start_date, '%Y-%m-%d')
    best = get_closest_hour(date_str, False)
    if best[1] < 1.4:
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

