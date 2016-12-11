import glob, os
import datetime
from eftel_data_filename import file_path

# Check whether or not we need to collect new data
dir_merged_data = file_path + 'Merged'
os.chdir(dir_merged_data)
last_date = glob.glob("*.csv")[0].split('_to_')[1][:10]
max_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

if last_date != max_date:
    # Collect queueing data from the last 2 weeks
    print 'Collecting Historical Queuing Times'
    import project_managament.shortest_path.data_collect

    print 'Merging Data'
    # Merge this data with all the previous
    import project_managament.shortest_path.efteling_data_merge

print 'Which algorithm do you want to use?'
print "Don't choose Permutations if you want more than 8 attractions"
answer = raw_input('Permutation (type P) or Genetic Algorithm (type GA) or Activity Crasher (AC): ')
answers = ['p', 'ga', 'ac']

while answer not in answers:
    print 'WRONG!!!! Please type in a correct answer.'
    answer = raw_input('Permutation (type P) or Genetic Algorithm (type GA) or Activity Crasher (AC): ')

if answer.lower() == 'p':
    import project_managament.shortest_path.shortest_path_perm_exact
elif answer.lower() == 'ga':
    import project_managament.genetic_PSO.genetic_runner
elif answer.lower() == 'ac':
    import project_managament.genetic_PSO.crash_it