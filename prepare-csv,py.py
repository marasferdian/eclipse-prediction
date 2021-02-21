import csv
from datetime import datetime, date, timedelta
from helper_functions import get_positions, convert_to_decimal_degrees
import pandas as pd

df = pd.read_csv('./solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(500)
eclipses_list = df['Date'].tolist()

with open('solar-eclipses-NN_2.csv', mode='w') as csv_file:
    fieldnames = ['Date', 'Moon Alt', 'Moon Az', 'Sun Alt', 'Sun Az', 'Is Eclipse']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    start_date = date(1900, 1, 1)
    end_date = date(2050, 12, 31)
    while start_date <= end_date:
        date_str = datetime.strftime(start_date, '%Y-%m-%d')
        moon_alt, moon_az, sun_alt, sun_az = get_positions(date_str)
        moon_alt = convert_to_decimal_degrees(str(moon_alt))
        moon_az = convert_to_decimal_degrees(str(moon_az))
        sun_alt = convert_to_decimal_degrees(str(sun_alt))
        sun_az = convert_to_decimal_degrees(str(sun_az))
        print(moon_alt, moon_az, sun_alt, sun_az)
        previous_date = start_date - timedelta(days=1)
        previous_date_str = datetime.strftime(previous_date,'%Y-%m-%d')
        isEclipse = date_str in eclipses_list or previous_date in eclipses_list
        writer.writerow({'Date': date_str, 'Moon Alt': moon_alt, 'Moon Az': moon_az, 'Sun Alt': sun_alt, 'Sun Az': sun_az, 'Is Eclipse': isEclipse})
        start_date += timedelta(days=1)
