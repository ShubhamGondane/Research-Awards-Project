import pandas as pd
import sys 

journal_file = sys.argv[1]
author_file = sys.argv[2]

jdf = pd.read_csv(journal_file)
titles_authors_df = jdf.groupby('title')['author_given'].apply(list).reset_index(name='author_given')
titles_authors_dict = {}

for title, authors in zip(titles_authors_df['title'], titles_authors_df['author_given']):
	titles_authors_dict[title] = authors

j_titles_authors_dict = titles_authors_dict

j_authors = set()
for k,v in j_titles_authors_dict.items():
	j_authors.add(val for val in v)


gdf = pd.read_csv(author_file)
total_authors_found = len(set(gdf['Author_id'].values.tolist()))

print("Total titles: {}\n Total titles found: {}\n Total authors: {}\n Total authors found: {}".format(total_titles, total_titles_found, total_authors, total_authors_found))