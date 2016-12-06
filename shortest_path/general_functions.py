import csv
import urllib2
from bs4 import BeautifulSoup
import datetime


def get_day_type(date):
    # Open feestdagen en check with the data
    dir_feestdagen = 'C:\\Users\\vande\\Dropbox\\Project Management\\Feestdagen.csv'
    with open(dir_feestdagen, 'rb') as f:
        reader = csv.reader(f)
        list_f = list(reader)[0]

    '''
    Assign day types
    1 = Feestdag
    2 = Weekend
    3 = Weekdag
    '''

    if date.strftime('%Y-%m-%d') in list_f:
        return 1
    elif date.isoweekday() > 5:
        return 2
    else:
        return 3


def round_to_5min(t):
    delta = datetime.timedelta(minutes=t.minute % 5,
                               seconds=t.second,
                               microseconds=t.microsecond)

    if delta > datetime.timedelta(minutes=2):
        diff = delta.seconds / 60
        t += datetime.timedelta(minutes=5 - diff)
    else:
        diff = delta.seconds / 60
        t -= datetime.timedelta(minutes=diff)
    return datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=0, microsecond=0)


def get_storingen():
    storingen = []
    a_url = 'http://eftelstats.nl/attractions.php?history=0'
    date = datetime.datetime.today()

    u = urllib2.urlopen(a_url).read()
    soup = BeautifulSoup(u, 'html.parser')
    table = soup.find_all("table", attrs={"class": "table table-striped"})[-1]

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    if datasets[0][0][1] != 'Geen':
        for a, b in datasets:
            storingen.append(a[1].encode('utf-8'))
    else:
        print 'Geen Storingen'

    return storingen

# time = datetime.datetime(year=2016, month=11, day=27, hour=8, minute=9)
# print round_to_5min(time)
