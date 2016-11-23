import itertools
import pandas as pd
from project_managament.progress_bar import print_progress

attractions = [u'JorisendeDraak', u'Baron1898',
               u'Droomvlucht', u'DeVliegendeHollander', u'Pirana', u'Python',
               u'CarnavalFestival', u'Stoomcarrousel', u'FataMorgana', u'Kleuterhof',
               u'VogelRok', u'VillaVolta', u'Bobbaan', u'HalveMaen', u'OudeTuffer',
               u'PandaDroom', u'MonsieurCannibale', u'Pagode', u'Kinderspoor',
               u'Gondoletta', u'KinderAvonturendoolhof', u'PolkaMarina', u'Spookslot',
               u'Diorama', u'Stoomtrein(Ruigrijk)', u'Stoomtrein(Marerijk)']

response = raw_input("Please enter nr of attractions: ")
attractions = attractions[:int(response)]
attractions_perm = itertools.permutations(attractions)

# Dataframe opstellen
dir_attr_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Afstanden.csv'
dir_attr_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Wandeltijden.csv'

attr_df = pd.read_csv(dir_attr_data)
attr_filter = ['Attr_Name'] + ['Ingang'] + list(attractions)
filter_length = len(attr_filter) - 1
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

# Empty
attr_distances = []
print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

for perm in attr_perm:
    count = 0
    total_distance = 0
    # Zoek afstand van Ingang naar eerste Attractie
    total_distance += attr_df.iloc[0][perm[0]]

    count = 0
    for p in perm:
        if p != perm[-1]:
            distance = attr_df.iloc[attractions.index(perm[count]) + 1][attractions.index(perm[count + 1]) + 2]
            total_distance += distance
            count += 1
    attr_distances.append({'permutation': perm, 'distance': total_distance})
    start += 1
    print_progress(start, stop, prefix='Progress:', suffix='Complete', barLength=50)

# Find the shortest path
min_perm = min(attr_distances, key=lambda x: x['distance'])

print min_perm
