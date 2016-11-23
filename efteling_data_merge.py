import glob, os
import pandas as pd
import csv
from dateutil import parser

dir_attr_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data'
os.chdir(dir_attr_data)

# Get all the .csv files
appended_data = []
for file in glob.glob("*.csv"):
    print file
    wacht_df = pd.read_csv('{0}\\{1}'.format(dir_attr_data, file))
    wacht_df = wacht_df.drop('Unnamed: 0', 1)
    appended_data.append(wacht_df)

appended_data = pd.concat(appended_data, axis=0)
# Put in dataframe & remove duplicates
wacht_df = pd.DataFrame(data=appended_data).drop_duplicates(keep=False)

# Open feestdagen en check with the data
dir_feestdagen = 'C:\\Users\\vande\\Dropbox\\Project Management\\Feestdagen.csv'
with open(dir_feestdagen, 'rb') as f:
    reader = csv.reader(f)
    list_f = list(reader)[0]

# Assign day types
list_day_type = []
for d in wacht_df['date']:
    # 1 = Feestdag
    # 2 = Weekend
    # 3 = Weekdag
    if d in list_f:
        list_day_type.append(1)
    elif parser.parse(d).isoweekday() > 5:
        list_day_type.append(2)
    else:
        list_day_type.append(3)

# Format dates
dates = pd.Series(data=wacht_df['date'])
dates = pd.to_datetime(dates)
wacht_df['date'] = dates

# Insert day_types
wacht_df['day_type'] = pd.Series(list_day_type, index=wacht_df.index)

# Sort by date
wacht_df = wacht_df.sort_values(by='date', ascending=True)

# Write to csv
wacht_df.to_csv('Merged\\efteling_data_from_{}_to_{}_with_day_types.csv'.format(wacht_df['date'].iloc[0].date(),
                                                                                wacht_df['date'].iloc[-1].date()))
