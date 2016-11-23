import itertools
import pandas as pd
import datetime
from project_managament.progress_bar import print_progress
from general_functions import get_day_type

# Assign start time
datetime.datetime.now()
# Assign which day type today is
day_type_today = get_day_type(datetime.date.today())

attractions = ['JorisendeDraak', 'Baron1898', 'Droomvlucht', 'DeVliegendeHollander', 'Pirana', 'Python',
               'CarnavalFestival', 'Stoomcarrousel', 'FataMorgana', 'Kleuterhof', 'VogelRok', 'VillaVolta',
               'Bobbaan', 'HalveMaen', 'OudeTuffer', 'PandaDroom', 'MonsieurCannibale', 'Pagode', 'Kinderspoor',
               'Gondoletta', 'KinderAvonturendoolhof', 'PolkaMarina', 'Spookslot', 'Diorama', 'Stoomtrein(Ruigrijk)',
               'Stoomtrein(Marerijk)']

response = raw_input("Please enter nr of attractions: ")
attractions = attractions[:int(response)]
attractions_perm = itertools.permutations(attractions)

# Dataframe opstellen
dir_afstand_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\afstanden.csv'
dir_wandel_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\wandeltijden.csv'

attr_df = pd.read_csv(dir_wandel_data, index_col=0)
attr_filter = ['Ingang'] + list(attractions)
filter_length = len(attr_filter)
attr_df = attr_df[attr_filter][:filter_length]

# Permutaties maken
attr_perm = []
perm_count = 0
for i in attractions_perm:
    attr_perm.append(i)
    perm_count += 1

start = 0
stop = perm_count
print 'Number of permutations: {0}'.format(perm_count)

# Read the data and use attractions as index
dir_duurtijd_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\General\\duurtijden_en_capaciteit.csv'
duurtijd_df = pd.read_csv(dir_duurtijd_data, index_col=0)

# Read the data and use as index
dir_wachttijd_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\Merged\\efteling_data_from_2016-11-02_to_2016-11-21_with_day_types.csv'
wachttijd_df = pd.read_csv(dir_wachttijd_data, index_col=0)

print wachttijd_df

# Empty distance array
attr_distances = []
print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

for perm in attr_perm:
    total_distance = 0
    # Zoek afstand van Ingang naar eerste Attractie
    total_distance += attr_df.iloc[0][perm[0]]

    count = 0
    for p in perm:
        if p != perm[-1]:
            distance = attr_df.ix[perm[count]][perm[count + 1]]
            duration = duurtijd_df.ix[p]['Tijd']
            total_distance += distance + duration
            count += 1
    attr_distances.append({'permutation': perm, 'distance': total_distance})
    start += 1
    print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Find the shortest path
min_perm = min(attr_distances, key=lambda x: x['distance'])

print min_perm
