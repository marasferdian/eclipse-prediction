import requests
import datetime
import os
import shutil
from bs4 import BeautifulSoup
file = open("C:/Users/Mara Sferdian/Downloads/solar-eclipses.txt","w",encoding="utf-8")
def nasa_eclipses_spider(start, end):
    if(start < 0):
        signStart = '-'
    else:
        signStart =''
    if(end <0):
        signEnd = '-'
    else:
        signEnd = ''
    if abs(start)<10:
        start =signStart+ '000'+str(abs(start))
    elif abs(start)>=10 and abs(start)<100:
        start=signStart+'00'+str(abs(start))
    elif abs(start)>=100 and abs(start)<1000:
        start = signStart+ '0'+str(abs(start))
    if abs(end)<10:
        end = signEnd+ '000'+str(abs(end))
    elif abs(end)>=10 and abs(end)<100:
        end=signEnd+'00'+str(abs(end))
    elif abs(end)>=100 and abs(end)<1000:
        end = signEnd+'0'+str(abs(end))
    url = 'https://eclipse.gsfc.nasa.gov/SEcat5/SE'+str(start)+'-'+str(end)+'.html'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for table in soup.findAll('pre'):
        print(table.get_text())
        file.write(table.get_text())


firstYear = -1999
lastYear = 2001
while firstYear <= lastYear:
    nasa_eclipses_spider(firstYear,firstYear + 99)
    #print(firstYear,firstYear + 99)
    firstYear+=100
file.close()
