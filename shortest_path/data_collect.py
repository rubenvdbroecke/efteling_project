import itertools
import urllib2
from bs4 import BeautifulSoup
import ast
from dateutil.parser import parse
import numpy as np
import pandas as pd
import datetime

dates = []
names = []
times = []
waiting = []

ran = xrange(0, 14)

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

    for i in x:
        list2 = np.array(categories)
        nr_of_rows = len(list2)
        list1 = [date] * nr_of_rows
        list3 = [i['name']] * nr_of_rows
        list4 = i['data']
        if len(list4) != nr_of_rows:
            list4 = [0] * nr_of_rows

        dates.append(list1)
        names.append(list3)
        times.append(list2)
        waiting.append(list4)

x = ({'date': list(itertools.chain(*dates)),
      'name': list(itertools.chain(*names)),
      'hour': list(itertools.chain(*times)),
      'waiting_time': list(itertools.chain(*waiting))})

names_attr = set(list(itertools.chain(*names)))

# storing_aantallen = []
# storing_tijden = []
# for i in names_attr:
#     print i
#     attr_name = i.lower().replace('(', '').replace(')', '')
#     a_url = 'http://eftelstats.nl/attraction.php?Id={0}'.format(attr_name)
#     u = urllib2.urlopen(a_url).read()
#     soup = BeautifulSoup(u, 'html.parser')
#     u = str(soup.get_text).rstrip().replace(' ', '')
#     stor = u.find('<h2>Storingen</h2>')
#     stor_a = u[stor + 170:].find('</td>')
#     storing_aantal = u[(stor + 170):(stor + 170 + stor_a)]
#     stor_b = u[(stor + 170 + stor_a + 9):].find('</td>')
#     storing_minuten = u[(stor + 170 + stor_a + 9): (stor + 170 + stor_a + 9 + stor_b)].replace('minuten', '')
#     storing_aantallen.append(storing_aantal)
#     # if not storing_aantal: storing_aantal = 0
#     # if not storing_minuten: storing_miuten = 0
#     date = datetime.date.today()
#     print date

a = (datetime.date.today() - datetime.timedelta(ran[0])).strftime("%Y-%m-%d").replace('-', '_')
b = (datetime.date.today() - datetime.timedelta(ran[-1])).strftime("%Y-%m-%d").replace('-', '_')

print b, a

dir_eft = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\efteling_data_from_{0}_to_{1}.csv'.format(b, a)
pd.DataFrame(x).to_csv(dir_eft)
