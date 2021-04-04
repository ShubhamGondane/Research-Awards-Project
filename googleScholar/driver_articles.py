from scholarly import scholarly
import pandas as pd
import time, random
from scholarly import ProxyGenerator
from tqdm import tqdm
import logging, pickle
from datetime import datetime
from pprint import pprint

pg = ProxyGenerator()
pg.Tor_Internal(tor_cmd = "/Applications/Tor Browser.app/Contents/MacOS/Tor/tor.real")
scholarly.use_proxy(pg)

no = {'26 Easy and Adorable Alphabet Recipes for Snacktime Quick, No-Cook Recipes with Instant Activities That Teach Each Letter of the Alphabet and Turn Snacktime Into Learning Time!'}
logging.basicConfig(filename='ss_article_author_script_errors.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('Run started at {}'.format(datetime.now()))

def read_csv(datafile):
	df = pd.read_csv(datafile)

	df['combined_title'] = df['title'] # + ": " + df['subtitle']
	# print(df.combined_title)
	titles =  list(set(df['combined_title'].values.tolist()))
	# print(len(titles))
	# exit()
	return titles
	# titles_authors_df = df.groupby('combined_title')['authors'].apply(list).reset_index(name='authors')
	# titles_authors_dict = {}

	# for title, authors in zip(titles_authors_df['combined_title'], titles_authors_df['authors']):
	# 	titles_authors_dict[title] = authors

	# return titles_authors_dict

input_file = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Journals_data/American Educational Research Journal.csv'

# Run for first time
titles = read_csv(input_file)
pickle_file = open('article_titles.pkl', 'wb')
pickle.dump(titles, pickle_file)

# pickle_file = open('article_titles.pkl', 'rb')
# titles = pickle.load(pickle_file)

def process_author(author, title):

	author_id = author.id
	author_name = author.name
	affiliation = author.affiliation
	interests  = author.interests
	citedby = author.citedby
	citedby5y = author.citedby5y
	hindex = author.hindex
	hindex5y = author.hindex5y
	i10index = author.i10index
	i10index5y = author.i10index5y

	# Dict object
	cites_per_year = author.cites_per_year

	publications = author.publications
	# print(publications)
	pubs_row = []

	for pub in publications:
		pub_year = ''
		if 'year' in pub.bib.keys():
			pub_year = pub.bib["year"]

		row = [author_id, pub.bib["cites"], pub.bib["title"], pub_year, pub.filled, pub.id_citations, pub.source]
		pubs_row.append(row)
	author_row = [title, author_id, author_name, affiliation, citedby, citedby5y, interests, hindex, hindex5y, i10index, i10index5y, cites_per_year]
	
	return author_row, pubs_row

def check_len(title):
	if len(title.split(" ")) < 10:
		return True
	return False
	# title = title.replace('"','')
	# if ":" in title:
	# 	sp = title.split(" : ")
	# 	if len(sp[0].split(" ")) > 15:
	# 		return False
	# elif len(title.split(" ")) > 15:
	# 	return False
	# else:
	# 	return True

def google_scholar_driver(input_list):
	rows = []
	publications = []
	input_list = [x for x in input_list if str(x) != 'nan']

# 548/595
	for k in tqdm(input_list, desc = 'Processing ...'):
		try:
			search_query, first_match = None, None
			found = False
			if k:
				search_query = scholarly.search_pubs(k)
				try:
					first_match = next(search_query).fill()
					if first_match.bib['ENTRYTYPE'] == 'article':
						author_ids = first_match.bib['author_id']
						
						for id_ in author_ids:
							if id_:
								author = scholarly.search_author_id(id_)
								author = author.fill()

								author_row, pubs_row = process_author(author, k)
								rows.append(author_row)
								publications.extend(pubs_row)
					found = True
					pickle_file = open('authors_AERA.pkl', 'wb')
					pickle.dump(rows, pickle_file)
					pickle_file.close()
				except StopIteration:
					logging.error('Title: {} raised StopIteration'.format(k))
				

			time.sleep(random.randint(3,9))
			print(len(publications))
			pub_df = pd.DataFrame(publications, columns=['Author_id','Cites','Title', 'Year','Filled', 'Id_citations', 'Source'])
			pub_df.to_csv('google_scholar_publications_AERA.csv', encoding = 'utf-8')

			if len(rows) % 50 == 0:
				pickle_file = open('authors_AERA.pkl', 'wb')
				pickle.dump(rows, pickle_file)
				pickle_file.close()
				# df = pd.DataFrame(rows, columns=['Title','Author_id','Author_name','Affiliation', 'CitedBy','CitedBy5y', 'Interests', 'h_index', 'h_index5y','i10_index','i10_index5y', 'Cites_per_year'])
				# df.to_csv('google_scholar_publications_JRLE.csv', encoding='utf-8')
				
				pub_df = pd.DataFrame(publications, columns=['Author_id','Cites','Title', 'Year','Filled', 'Id_citations', 'Source'])
				pub_df.to_csv('google_scholar_publications_AERA.csv', encoding = 'utf-8')

		except Exception as e:
			logging.error('Title: {} raised the following errors'.format(k))
			if not found:
				logging.error('Did not find the following title  '.format(k))

			logging.error('{}'.format(e))

	pickle_file = open('authors_AERA.pkl', 'wb')
	pickle.dump(rows, pickle_file)
	pickle_file.close()
	# df = pd.DataFrame(rows, columns=['Title','Author_id','Author_name','Affiliation', 'CitedBy','CitedBy5y', 'Interests', 'h_index', 'h_index5y','i10_index','i10_index5y', 'Cites_per_year'])
	# df.to_csv('google_scholar_publications_JRLE.csv', encoding='utf-8')

	pub_df = pd.DataFrame(publications, columns=['Author_id','Cites','Title', 'Year','Filled', 'Id_citations', 'Source'])
	pub_df.to_csv('google_scholar_publications_AERA.csv', encoding = 'utf-8')


google_scholar_driver(titles)
