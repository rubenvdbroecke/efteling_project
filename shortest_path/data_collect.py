import itertools
import urllib2
from bs4 import BeautifulSoup
import ast
from dateutil.parser import parse
import numpy as np
import pandas as pd
import datetime
from project_managament.eftel_data_filename import file_path


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

x = ({'date': list(itertools.chain(*dates)),
      'name': list(itertools.chain(*names)),
      'hour': list(itertools.chain(*times)),
      'waiting_time': list(itertools.chain(*waiting))})

names_attr = set(list(itertools.chain(*names)))

a = (datetime.date.today() - datetime.timedelta(ran[0])).strftime("%Y-%m-%d").replace('-', '_')
b = (datetime.date.today() - datetime.timedelta(ran[-1])).strftime("%Y-%m-%d").replace('-', '_')

print b, a


dir_eft = file_path + 'efteling_data_from_{0}_to_{1}.csv'.format(b, a)
pd.DataFrame(x).to_csv(dir_eft)
