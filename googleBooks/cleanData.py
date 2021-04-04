import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
from ast import literal_eval
from numpy import nan
from tqdm import tqdm 


path_ = '/Users/shubhamgondane/volunteer_work/data/book_publishers_data/'
book_files = [f for f in listdir(path_) if isfile(join(path_, f)) and f != '.DS_Store']

columns_to_drop = ['Unnamed: 0', 'readingModes','allowAnonLogging','contentVersion', 'imageLinks', 'panelizationSummary']
columns_with_list_elements = ['authors', 'industryIdentifiers', 'categories']

def clean_one(file):

	df = pd.read_csv(file)

	# Drop useless columns
	for col in columns_to_drop:
		if col in df.columns.values.tolist():
			df = df.drop([col], axis=1)

	# Convert string to list for some columns
	for col in columns_with_list_elements:
		df[col] = df[col].fillna("[]")
		df[col] = df[col].apply(literal_eval)

	df = df.explode('authors')
	return df
def clean_categories(df):
	categories = df['categories'].values.tolist()
	cleaned = []
	for category in categories:
		if category:
			cleaned.append(''.join(category))
		else:
			cleaned.append("")
		# 	c = category[0].split("'")[1:-1]
		# 	print(c)
		# 	exit()
		# 	if len(c) != 0:
		# 		cleaned.append(c[0])
		# 	else:
		# 		cleaned.append("")

			
		
	df['categories'] = cleaned
	return df



for file in tqdm(book_files):
	print(file)
	clean_df = clean_one(path_+file)
	clean_df = clean_categories(clean_df)
	new_path = path_ + 'cleaned/' 
	clean_df.to_csv(new_path+file, encoding='utf-8')
	





















