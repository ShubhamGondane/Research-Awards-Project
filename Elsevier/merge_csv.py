import pandas as pd
import sys
from os import listdir
from os.path import isfile, join

folder_path = sys.argv[1]
output_file = 'final_tweets.csv'
files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
frames = []

for file in files:
	df = pd.read_csv(folder_path+"/"+file)
	frames.append(df)

final_df = pd.concat(frames)
final_df.drop_duplicates(keep='first',inplace=True) 
final_df.to_csv(folder_path+"/"+output_file)


