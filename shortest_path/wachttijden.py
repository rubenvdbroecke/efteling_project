import csv
import pandas as pd


dir_wachttijd_data = 'C:\\Users\\vande\\Dropbox\\Project Management\\Efteling Data\\Wachttijden\\wachttijden_en_capaciteit.csv'

# Read the data and use attractions as index
wachttijd_df = pd.read_csv(dir_wachttijd_data, index_col=0)

print wachttijd_df.ix['JorisendeDraak']['Tijd']