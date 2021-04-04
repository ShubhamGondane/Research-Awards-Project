import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
from ast import literal_eval
from numpy import nan
from tqdm import tqdm 


path_ = '~/volunteer_work/data/article_journals_data/'
book_files = [f for f in listdir(path_) if isfile(join(path_, f)) and f != '.DS_Store']

columns_to_drop = []
columns_with_list_elements = ['ISSN', 'alternative-id', 'container-title', 'date-parts', 'domain', 'short-container-title', 'subject', 'subtitle', 'title']

def clean_one(file):

	df = pd.read_csv(file)
	print(df.shape)
	# print(df.columns.tolist())
	
	# # Drop useless columns
	# for col in columns_to_drop:
	# 	if col in df.columns.values.tolist():
	# 		df = df.drop([col], axis=1)

	# Convert string to list for some columns
	for col in columns_with_list_elements:
		if col in df.columns.values.tolist():
			df[col] = df[col].fillna("[]")
			df[col] = df[col].apply(literal_eval)
			if col != 'ISSN' and col != 'date-parts':
				df = df.explode(col)

	print(df.shape)
	return df

for file in tqdm(book_files):
	print(file)
	clean_df = clean_one(path_+file)
	new_path = path_ + 'cleaned/' 
	clean_df.to_csv(new_path+file, encoding='utf-8')
	



