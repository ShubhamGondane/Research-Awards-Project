import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
from ast import literal_eval
from numpy import nan
from tqdm import tqdm 
from pprint import pprint

path_ = '/Users/shubhamgondane/volunteer_work/data/book_publishers_data/books_data/'
book_files = [f for f in listdir(path_) if isfile(join(path_, f)) and f != '.DS_Store']

dfs = []
for file in tqdm(book_files):
	
	df = pd.read_csv(path_+file)
	print(df.shape)
	dfs.append(df)

final_df = pd.concat(dfs, ignore_index = True)

# print(final_df.shape)
print(final_df.isnull().sum())

# ddf = final_df.groupby('categories')['title'].nunique().sort_values(ascending=False)
# ddf.to_csv('/Users/shubhamgondane/volunteer_work/data/descriptive_statistics.csv')