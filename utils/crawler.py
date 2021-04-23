import requests
import datetime
import os
import shutil
from bs4 import BeautifulSoup
#headers = requests.utils.default_headers()
#headers.update({
#    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
#})
months = {'january': '01', 'february': '02', 'march': '03', 'april': '04', 'may': '05', 'june': '06', 'july': '07', 'august': '08', 'september': '09',
'october': '10', 'november': '11', 'december': '12'}
def eclipses_spider(max_starty, region):
    solar_eclipses = []
    lunar_eclipses = []
    transit_eclipses = []
    starty = 1900
    while starty <= max_starty:
        url = 'http://www.timeanddate.com/eclipse/list.html?region='+ region+'&starty=' + str(starty)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'class':'ec-link'}):
            href = link.get('href').split('/')
            type = href[2]
            date = href[3]
            split_date = date.split('-')
            split_date[1] = months[split_date[1]]
            date = '-'.join(split_date)
            #formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            location = link.findChildren("span" ,{'class': 'ec-where'}, recursive=False)[0].get_text()
            name = link.findChildren("span" ,{'class': 'ec-type'}, recursive=False)[0]
            type_of_eclipse = name.findChildren("span" ,{'class': 'sub'}, recursive=False)[0].get_text()
            type_of_eclipse = type_of_eclipse.replace('(','')
            type_of_eclipse = type_of_eclipse.replace(')','')
            if type == 'solar':
                solar_eclipses.append([region,type_of_eclipse, date, location])
            elif type == 'lunar':
                lunar_eclipses.append([region,type_of_eclipse, date, location])
            else:
                transit_eclipses.append([region,type_of_eclipse, date, location])
        starty += 10
    print('!!!ECLIPSES IN '+ region.upper() + '!!!!!')
    print('------SOLAR ECLIPSES--------')
    for eclipse in solar_eclipses:
        print(eclipse)
    print('\n')
    print('-----LUNAR ECLIPSES---------')
    for eclipse in lunar_eclipses:
        print(eclipse)
    print('\n')
    print('-------TRANSITS-----------')
    for eclipse in transit_eclipses:
        print(eclipse)
    print('\n')
    print('solar eclipses: '+ str(len(solar_eclipses)))
    print('lunar eclipses: '+ str(len(lunar_eclipses)))
    print('transit eclipses: '+ str(len(transit_eclipses)))


regions = ['africa', 'asia', 'antarctica','atlantic','arctic', 'australia', 'europe', 'indian-ocean','north-america','pacific', 'south-america']
for i in range(len(regions)):
    eclipses_spider(2010,regions[i])
