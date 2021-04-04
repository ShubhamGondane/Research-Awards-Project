import pandas as pd
from os import listdir
from os.path import isfile, join
from tqdm import tqdm 

path_ = '/Users/shubhamgondane/volunteer_work/data/book_publishers_data/books_data/'
book_files = [f for f in listdir(path_) if isfile(join(path_, f)) and f != '.DS_Store']

dfs = []
for file in tqdm(book_files):
	
	df = pd.read_csv(path_+file)
	print(df.shape)
	dfs.append(df)

final_df = pd.concat(dfs, ignore_index = True)
# print(final_df.shape)
# print(final_df.describe())
education_df = final_df.loc[final_df['categories'] == 'Education']
education_df = education_df.drop(['Unnamed: 0'], axis = 1)
education_df.reset_index(drop=True, inplace=True)
print(education_df.shape)
# education_df.to_csv('/Users/shubhamgondane/volunteer_work/data/analysis/Education_books.csv')

socialscience_df = final_df.loc[final_df['categories'] == 'Social Science']
socialscience_df = socialscience_df.drop(['Unnamed: 0'], axis = 1)
socialscience_df.reset_index(drop=True, inplace=True)
print(socialscience_df.shape)
# socialscience_df.to_csv('/Users/shubhamgondane/volunteer_work/data/analysis/Social_Science_books.csv')

