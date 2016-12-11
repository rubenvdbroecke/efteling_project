import sys
import glob
import itertools
import pandas as pd
import datetime
import os
from project_managament.progress_bar import print_progress
from general_functions import get_day_type, round_to_5min, get_storingen
from project_managament.eftel_data_filename import file_path
from random import shuffle
import ast
from efteling_journey import generate_journey

attractions = ['JorisendeDraak', 'Baron1898', 'Droomvlucht', 'DeVliegendeHollander', 'Pirana', 'Python',
               'CarnavalFestival', 'Stoomcarrousel', 'FataMorgana', 'Kleuterhof', 'VogelRok', 'VillaVolta',
               'Bobbaan', 'HalveMaen', 'OudeTuffer', 'PandaDroom', 'MonsieurCannibale', 'Pagode', 'Kinderspoor',
               'Gondoletta', 'KinderAvonturendoolhof', 'PolkaMarina', 'Spookslot', 'Diorama', 'Stoomtrein(Ruigrijk)',
               'Stoomtrein(Marerijk)']

for a in get_storingen():
    attractions.remove(a)

response = raw_input("Please enter nr of attractions: ") or 5

st = datetime.datetime.now()
# shuffle(attractions)
attractions = attractions[:int(response)]

# For custom user input (samples)
# list_index = x = ast.literal_eval(response)
# attractions = list(attractions[i] for i in list(i - 1 for i in list_index))

# Permutaties maken
attr_perm = list(itertools.permutations(attractions))

# Dataframe opstellen
dir_wandel_data = file_path + '/General/wandeltijden.csv'

attr_df = pd.read_csv(dir_wandel_data, index_col=0)
attr_filter = ['Ingang'] + list(attractions)
filter_length = len(attr_filter)
attr_df = attr_df[attr_filter]

start = 0
stop = len(attr_perm)

print 'Number of attractions: {0} {1}\n' \
      'Number of permutations: {2}\n'.format(len(attractions), attractions, len(attr_perm))

# Read the duration data and use attractions as index
dir_duurtijd_data = file_path + 'General/duurtijden_en_capaciteit.csv'
duurtijd_df = pd.read_csv(dir_duurtijd_data, index_col=0)

# Read the waiting time data
dir_merged_data = file_path + '/Merged'
dir_wachttijd_data = glob.glob(dir_merged_data + "\\*.csv")[0].replace('\\', '\\\\')
wachttijd_df = pd.read_csv(dir_wachttijd_data, index_col=0)
# Change variable name of 'hour'
wachttijd_df = wachttijd_df.rename(columns={'hour': 'time'})
# Create new variable, for grouping purposes
wachttijd_df['hour'] = [i[:2] for i in wachttijd_df['time']]
# Group the data , day_type , name and hour
grouped_data = wachttijd_df.groupby(['day_type', 'name', 'time'], as_index=False).mean()
# grouped_data = wachttijd_df.groupby(['day_type', 'name', 'hour'], as_index=False).mean()

# print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Empty distance array
attr_distances = []

# Assign which day type today is
day_type_today = get_day_type(datetime.date.today())
# For custom user input
# ham = raw_input('Enter hour and minute: ').split('u')

for perm in attr_perm:
    sys.stdout.write('\r{0}/{1}'.format(start, stop))
    leave_time = now = datetime.datetime.now()
    # For custom user input
    # leave_time = now = datetime.datetime(year=2016, month=12, day=6, hour=int(ham[0]), minute=int(ham[1]), second=0)

    # Assign start time
    start_time = now
    # print 'Start time of the visit: {0}'.format(start_time)

    total_duration = 0
    # Zoek duration van Ingang naar eerste Attractie
    total_duration += attr_df.iloc[0][perm[0]]
    arr_time = start_time + datetime.timedelta(minutes=attr_df.iloc[0][perm[0]])
    # print 'WALKING time from Entrance to {0} : {1}'.format(perm[0], attr_df.iloc[0][perm[0]])
    try:
        waiting_time = grouped_data.loc[
            (grouped_data['day_type'] == day_type_today) & (grouped_data['name'] == perm[0]) & (
                grouped_data['time'] == round_to_5min(arr_time).strftime('%H:%M:00'))]['waiting_time'].values[0]
    except IndexError:
        waiting_time = 0

    # print 'WAITING time of {0} is {1} minutes on {2}'.format(perm[0], waiting_time, round_to_5min(arr_time).strftime('%H:%M'))
    start_time += datetime.timedelta(minutes=waiting_time + attr_df.iloc[0][perm[0]])

    count = 0
    visiting_hours = [start_time]
    attraction_time = [float(duurtijd_df.ix[perm[0]]['Tijd']) / 60]
    travel_time = [attr_df.iloc[0][perm[0]]]
    queuing_time = [0]

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
                        grouped_data['time'] == round_to_5min(arr_time).strftime('%H:%M:00'))]['waiting_time'].values[0]
            except IndexError:
                for i in xrange(100):
                    idx = grouped_data[(grouped_data['day_type'] == day_type_today) & (grouped_data['name'] == perm[count + 1]) & (
                        grouped_data['time'] == (round_to_5min(arr_time) - datetime.timedelta(minutes=i * 5)).strftime('%H:%M:00'))].index.tolist()
                    if len(idx) > 0:
                        waiting_time = grouped_data.loc[idx[0]]['waiting_time']
                        idx = []
                        break

            # print 'WAITING time of {0} is {1} minutes on {2}'.format(perm[count + 1], waiting_time, round_to_5min(arr_time).strftime('%H:%M'))

            arr_time += datetime.timedelta(minutes=waiting_time)
            visiting_hours.append(arr_time)
            attraction_time.append(float(duurtijd_df.ix[perm[count + 1]]['Tijd']) / 60)
            travel_time.append(attr_df.ix[perm[count]][perm[count + 1]])
            queuing_time.append(waiting_time)

            # print 'Arrive in {0} at {1}'.format(perm[count + 1], arr_time)
            start_time = arr_time + datetime.timedelta(minutes=float(duurtijd_df.ix[perm[count + 1]]['Tijd']) / 60)
            # print 'Leave {0} at {1}'.format(perm[count + 1], start_time)
            leave_time = start_time
            count += 1

    total_duration = float((leave_time - now).total_seconds()) / 60

    attr_distances.append(
        {'permutation': perm, 'duration': total_duration, 'visiting_hours': visiting_hours, 'start': now,
         'attraction_time': attraction_time, 'travel_time': travel_time, 'queuing_time': queuing_time})

    start += 1
    # print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Find the shortest path
min_perm = min(attr_distances, key=lambda x: x['duration'])
print datetime.datetime.now() - st
print 'Attractions:'
print '\t{0}: Entrance'.format(min_perm['start'].strftime('%Hu%M'))
for i in xrange(len(min_perm['permutation'])):
    print '\t{0}: {1}\tTw: {2}\tTq: {3}\tTa:{4}'.format(min_perm['visiting_hours'][i].strftime('%Hu%M'),
                                                       min_perm['permutation'][i],
                                                       min_perm['travel_time'][i],
                                                       min_perm['queuing_time'][i],
                                                       min_perm['attraction_time'][i]
                                                       )

print '\nEnd of Journey: {0}'.format((min_perm['visiting_hours'][-1] + datetime.timedelta(minutes=int(min_perm['attraction_time'][-1]))).strftime('%H:%M'))
print 'Total Duration: {0} minutes'.format(round(min_perm['duration'], 2))

# Pass the sequence to generate map (only works for the first 8 attractions(for now))
a_s = ['Entrance'] + list(min_perm['permutation'])
generate_journey(a_s)

