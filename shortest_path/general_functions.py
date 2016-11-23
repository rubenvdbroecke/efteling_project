import csv
from dateutil import parser
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

    t -= delta
    if delta > datetime.timedelta(minutes=2):
        t += datetime.timedelta(minutes=5)
    else:
        t -= datetime.timedelta(minutes=t.minute)
    return t

