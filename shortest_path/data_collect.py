import itertools
import urllib2
from bs4 import BeautifulSoup
import ast
from dateutil.parser import parse
import numpy as np
import pandas as pd
import datetime
import csv

dates = []
names = []
times = []
waiting = []
storingen = []

ran = xrange(1, 14)

for i in ran:
    url = 'http://eftelstats.nl/attractions.php?history={0}'.format(i)
    print url

    u = urllib2.urlopen(url).read()
    soup = BeautifulSoup(u, 'html.parser')
    u = str(soup.get_text).rstrip().replace(" ", "")

    date = datetime.date.today() - datetime.timedelta(i)
    print date

    a = u.find('categories:')
    b = u.find('yAxis')

    categories = u[(a + 11):(b - 4)]
    x = ast.literal_eval(categories)
    categories = [parse(n).time() for n in x]

    a = u.find('series:')
    b = u.find('exporting:')

    attractions = u[(a + 7):(b - 3)]

    x = ast.literal_eval(attractions)

    for r in x:
        list2 = np.array(categories)
        nr_of_rows = len(list2)
        list1 = [date] * nr_of_rows
        list3 = [r['name']] * nr_of_rows
        list4 = r['data']
        if len(list4) != nr_of_rows:
            list4 = [0] * nr_of_rows

        dates.append(list1)
        names.append(list3)
        times.append(list2)
        waiting.append(list4)

    a_url = 'http://eftelstats.nl/dayreport.php?history={}'.format(i)
    print a_url
    u = urllib2.urlopen(a_url).read()
    soup = BeautifulSoup(u, 'html.parser')
    try:
        table = soup.find("table", attrs={"class": "table table-striped"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for a, b, c in datasets:
            attr_name = a[1]
            try:
                start_storing = parse(b[1]).time()
                start_storing_td = datetime.timedelta(hours=start_storing.hour, minutes=start_storing.minute)
                eind_storing = parse(c[1]).time()
                eind_storing_td = datetime.timedelta(hours=eind_storing.hour, minutes=eind_storing.minute)
            except ValueError:
                if date.weekday() > 4:
                    eind_storing = datetime.time(hour=19, minute=0)
                    eind_storing_td = datetime.timedelta(hours=19, minutes=0)
                else:
                    eind_storing = datetime.time(hour=18, minute=0)
                    eind_storing_td = datetime.timedelta(hours=18, minutes=0)

            difference = (eind_storing_td - start_storing_td).seconds / 60

            storingen.append({'name': attr_name,
                              'date': date,
                              'start_storing': start_storing,
                              'stop_storing': eind_storing,
                              'time_diff': difference})
    except AttributeError:
        print 'No Data To Show'
        storingen.append({'name': '',
                          'date': '',
                          'start_storing': 0,
                          'stop_storing': 0,
                          'time_diff': 0})


x = ({'date': list(itertools.chain(*dates)),
      'name': list(itertools.chain(*names)),
      'hour': list(itertools.chain(*times)),
      'waiting_time': list(itertools.chain(*waiting))})

names_attr = set(list(itertools.chain(*names)))

a = (datetime.date.today() - datetime.timedelta(ran[0])).strftime("%Y-%m-%d").replace('-', '_')
b = (datetime.date.today() - datetime.timedelta(ran[-1])).strftime("%Y-%m-%d").replace('-', '_')

print b, a

dir_eft = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\efteling_data_from_{0}_to_{1}.csv'.format(b, a)
pd.DataFrame(x).to_csv(dir_eft)

names = []
dates = []
start_storingen = []
stop_storingen = []
differences = []

for s in storingen:
    names.append(s['name'])
    dates.append(s['date'])
    start_storingen.append(s['start_storing'])
    stop_storingen.append(s['stop_storing'])
    differences.append(s['time_diff'])

y = ({'date': dates,
      'name': names,
      'start_storing': start_storingen,
      'stop_storing': stop_storingen,
      'time_diff': differences})

dir_eft = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\efteling_storing_data_from_{0}_to_{1}.csv'.format(b, a)
pd.DataFrame(y).to_csv(dir_eft)
