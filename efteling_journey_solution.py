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
answer = raw_input('Permutation (type P) or Genetic Algorithm (type GA): ')

if answer == 'P':
    import project_managament.shortest_path.shortest_path_perm_exact
else:
    # Import the script it should perform
    print ''