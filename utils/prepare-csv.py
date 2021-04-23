import csv
from datetime import datetime, date, timedelta
from helper_functions import get_minimum_separation
import pandas as pd

df = pd.read_csv('../numerical_methods/solar-eclipses.csv', parse_dates=['Date'])
df = df.tail(500)
eclipses_list = df['Date'].tolist()

with open('../ML/solar-eclipses-classif.csv', mode='w') as csv_file:
    fieldnames = ['Date', 'Separation', 'Is Eclipse']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    start_date = date(1950, 1, 1)
    end_date = date(2100, 12, 31)
    while start_date <= end_date:
        date_str = datetime.strftime(start_date, '%Y-%m-%d')
        sep = get_minimum_separation(date_str)
        isEclipse = date_str in eclipses_list
        writer.writerow({'Date': date_str, 'Separation': sep, 'Is Eclipse': isEclipse})
        print(date_str)
        start_date += timedelta(days=1)
