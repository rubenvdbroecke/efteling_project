import itertools
import pandas as pd
import datetime
from project_managament.progress_bar import print_progress
from general_functions import get_day_type, round_to_5min
from random import shuffle

attractions = ['JorisendeDraak', 'Baron1898', 'Droomvlucht', 'DeVliegendeHollander', 'Pirana', 'Python',
               'CarnavalFestival', 'Stoomcarrousel', 'FataMorgana', 'Kleuterhof', 'VogelRok', 'VillaVolta',
               'Bobbaan', 'HalveMaen', 'OudeTuffer', 'PandaDroom', 'MonsieurCannibale', 'Pagode', 'Kinderspoor',
               'Gondoletta', 'KinderAvonturendoolhof', 'PolkaMarina', 'Spookslot', 'Diorama', 'Stoomtrein(Ruigrijk)',
               'Stoomtrein(Marerijk)']

response = raw_input("Please enter nr of attractions: ") or 5

shuffle(attractions)
attractions = attractions[:int(response)]

# Permutaties maken
attr_perm = list(itertools.permutations(attractions))

# Dataframe opstellen
# dir_afstand_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\afstanden.csv'
dir_wandel_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\wandeltijden.csv'

attr_df = pd.read_csv(dir_wandel_data, index_col=0)
attr_filter = ['Ingang'] + list(attractions)
filter_length = len(attr_filter)
attr_df = attr_df[attr_filter]

start = 0
stop = len(attr_perm)

print 'Number of attractions: {0} {1}\n' \
      'Number of permutations: {2}\n'.format(len(attractions), attractions, len(attr_perm))

# Read the duration data and use attractions as index
dir_duurtijd_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\duurtijden_en_capaciteit.csv'
duurtijd_df = pd.read_csv(dir_duurtijd_data, index_col=0)

# Read the waiting time data
dir_wachttijd_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\Merged\\efteling_data_from_2016-11-02_to_2016-11-21_with_day_types.csv'
wachttijd_df = pd.read_csv(dir_wachttijd_data, index_col=0)
# Change variable name of 'hour'
wachttijd_df = wachttijd_df.rename(columns={'hour': 'time'})
# Create new variable, for grouping purposes
wachttijd_df['hour'] = [i[:2] for i in wachttijd_df['time']]
# Group the data , day_type , name and hour
grouped_data = wachttijd_df.groupby(['day_type', 'name', 'hour'], as_index=False).mean()

print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Empty distance array
attr_distances = []

for perm in attr_perm:
    leave_time = now = datetime.datetime.now()
    # Assign start time
    start_time = now
    # print 'Start time of the visit: {0}'.format(start_time)
    # Assign which day type today is
    day_type_today = get_day_type(datetime.date.today())

    total_duration = 0
    # Zoek duration van Ingang naar eerste Attractie
    total_duration += attr_df.iloc[0][perm[0]]
    arr_time = start_time + datetime.timedelta(minutes=attr_df.iloc[0][perm[0]])
    # print 'WALKING time from Entrance to {0} : {1}'.format(perm[0], attr_df.iloc[0][perm[0]])
    try:
        waiting_time = grouped_data.loc[
            (grouped_data['day_type'] == day_type_today) & (grouped_data['name'] == perm[0]) & (
                grouped_data['hour'] == round_to_5min(arr_time).strftime('%H'))]['waiting_time'].values[0]
    except IndexError:
        waiting_time = 0

    # print 'WAITING time of {0} is {1} minutes'.format(perm[0], waiting_time)
    start_time += datetime.timedelta(minutes=waiting_time + attr_df.iloc[0][perm[0]])

    count = 0
    visiting_hours = [start_time]

    # print 'Arrive in {0} at {1}'.format(perm[0], start_time)
    start_time += datetime.timedelta(minutes=float(duurtijd_df.ix[perm[0]]['Tijd']) / 60)
    # print 'Leave {0} at {1}'.format(perm[0], start_time)

    for p in perm:
        if p != perm[-1]:
            # Calculate different durations
            walking_duration = attr_df.ix[perm[count]][perm[count + 1]]

            arr_time = start_time + datetime.timedelta(minutes=walking_duration)

            # print 'WALKING time from {0} to {1} is {2} minutes'.format(perm[count], perm[count + 1], walking_duration)

            try:
                waiting_time = grouped_data.loc[
                    (grouped_data['day_type'] == day_type_today) & (grouped_data['name'] == perm[count + 1]) & (
                        grouped_data['hour'] == round_to_5min(arr_time).strftime('%H'))]['waiting_time'].values[0]
            except IndexError:
                waiting_time = 0

            # print 'WAITING time of {0} is {1} minutes'.format(perm[count + 1], waiting_time)

            arr_time += datetime.timedelta(minutes=waiting_time)
            visiting_hours.append(arr_time)

            # print 'Arrive in {0} at {1}'.format(perm[count + 1], arr_time)
            start_time = arr_time + datetime.timedelta(minutes=float(duurtijd_df.ix[perm[count + 1]]['Tijd']) / 60)
            # print 'Leave {0} at {1}'.format(perm[count + 1], start_time)
            leave_time = start_time
            count += 1

    total_duration = float((leave_time - now).total_seconds()) / 60

    attr_distances.append(
        {'permutation': perm, 'duration': total_duration, 'visiting_hours': visiting_hours, 'start': now})

    start += 1
    print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Find the shortest path
min_perm = min(attr_distances, key=lambda x: x['duration'])

print 'Attractions:'
print '\t{0}: Entrance'.format(min_perm['start'].strftime('%Hu%M'))
for i in xrange(len(min_perm['permutation'])):
    print '\t{0}: {1}'.format(min_perm['visiting_hours'][i].strftime('%Hu%M'), min_perm['permutation'][i])

print '\nTotal Duration: {0} minutes'.format(round(min_perm['duration'], 2))
