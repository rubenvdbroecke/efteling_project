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

    if delta > datetime.timedelta(minutes=2):
        diff = delta.seconds / 60
        t += datetime.timedelta(minutes=5 - diff)
    else:
        diff = delta.seconds / 60
        t -= datetime.timedelta(minutes=diff)
    return datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=0, microsecond=0)


# time = datetime.datetime(year=2016, month=11, day=27, hour=8, minute=9)
# print round_to_5min(time)
