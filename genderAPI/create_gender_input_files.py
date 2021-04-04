from os import listdir
from os.path import isfile, join
import pandas as pd
import unicodedata


# journals_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Authors_data/Scopus Author/'
# journals = [f for f in listdir(journals_path) if isfile(join(journals_path, f)) and f not in ['.DS_Store']]


# for journal in journals:
# 	df = pd.read_csv(journals_path+journal, encoding='utf-8')
# 	new = df["Given_name"].str.split(" ", n = 1, expand = True)
# 	df["first_name"] = new[0] 
# 	df.to_csv(journals_path+'Gender_input/'+journal+'_gender.csv', encoding='utf-8')


book_df = pd.read_csv("/Users/shubhamgondane/volunteer_work/data/book_publishers_data/authors_data/google_scholar_educational.csv")
new = book_df["Author_name"].str.split(" ", n=1, expand = True)
book_df["first_name"] = new[0]
book_df.to_csv("/Users/shubhamgondane/volunteer_work/data/book_publishers_data/authors_data/Gender_input/google_scholar_educational.csv")


book_df = pd.read_csv("/Users/shubhamgondane/volunteer_work/data/book_publishers_data/authors_data/google_scholar_socialscience.csv")
new = book_df["Author_name"].str.split(" ", n=1, expand = True)
book_df["first_name"] = new[0]
book_df.to_csv("/Users/shubhamgondane/volunteer_work/data/book_publishers_data/authors_data/Gender_input/google_scholar_socialscience.csv")

