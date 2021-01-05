import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
import datetime as dt
from datetime import date
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot

df = pd.read_csv('C:/Users/Mara Sferdian/Downloads/thesis/solar-eclipses.csv', parse_dates = ['Date'])
df = df.tail(1000)

#for moon
x = []
#for sun
y = []
list = df['Date'].tolist()
x.append(0)
y.append(0)
date_format = '%Y-%m-%d'
moonCycleLength = 27.321662
solarCycleLength = 365.25636
firstDate = datetime.strptime(list[0], date_format)
for i in range(1, len(list)):
        date = datetime.strptime(list[i], date_format)
        delta = date - firstDate
        difference = delta.days
        x.append(difference % moonCycleLength)
        y.append(difference % solarCycleLength)
x_no_corner_cases = []
y_no_corner_cases = []
used_dates = []
for i in range (1000):
    raport = 0
    if i != 0:
        raport = y[i]/x[i]
        if not (raport < 1 or raport > 1000):
            x_no_corner_cases.append(x[i])
            y_no_corner_cases.append(y[i])
            used_dates.append(list[i])
covariance = np.cov(x_no_corner_cases,y_no_corner_cases)
corr, _ = pearsonr(x_no_corner_cases,y_no_corner_cases)
print('Pearsons correlation: %.3f' % corr)
x_no_corner_cases = np.array(x_no_corner_cases)
y_no_corner_cases = np.array(y_no_corner_cases)
print('Cases included: '+ str(len(x_no_corner_cases)) + ' out of 1000')
m, b = np.polyfit(x_no_corner_cases, y_no_corner_cases, 1)
plt.plot(x_no_corner_cases, y_no_corner_cases, 'o')
plt.plot(x_no_corner_cases, m*x_no_corner_cases + b)
plt.show()
#data = np.array([x_no_corner_cases, y_no_corner_cases])
dataset = pd.DataFrame({'Moon Cycle Day (x)': x_no_corner_cases, 'Solar Cycle Day (y)': y_no_corner_cases}, index = used_dates)
dataset.index.name = 'Date'
print(dataset.head(2))
autocorrelation_plot(dataset)
pyplot.show()
plot_acf(dataset)
pyplot.show()
