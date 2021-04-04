from pybliometrics.scopus import AbstractRetrieval, ScopusSearch, AuthorRetrieval
import pandas as pd
import time
from datetime import date
from tqdm import tqdm 
from os import listdir
from os.path import isfile, join
import logging
import pickle

journals_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Journals_data/'
authors_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Authors_data/'
journals = [f for f in listdir(journals_path) if isfile(join(journals_path, f)) and f not in ['.DS_Store',
										'Comparative Education Review.csv',
										'Journal of Research on Leadership Education.csv',
										'Educational Administration Quarterly.csv',
										'Journal of Educational and Behavioral Statistics_1.csv',
										'Journal of Educational and Behavioral Statistics.csv',
										'Journal of Educational and Behavioral Statistics_2.csv',
										'Educational Evaluation and Policy Analysis.csv']]

columns = ['Author_id', 'ORCID', 'Given_name','Surname', 'Current_affiliation_id', 'Current_affiliation_name', 'Awards_won', 'H_index', 'Citation_count' ,'Cited_by_count', 'Publication_range', 'Subject_areas']
author_columns = ['Author_id', 'ORCID', 'Past_affiliation_id', 'Past_affiliation_name']

logging.basicConfig(filename='author_script_errors.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('Run started at {}'.format(date.today()))

def process_journal(file):
	logging.warning('Getting data for {}'.format(file))

	df = pd.read_csv(journals_path+file)
	dois = df['DOI'].unique()

	rows = []
	author_rows = []
	authors_set = set()
	print("Processing DOIs...")
	for doi in tqdm(dois):
		try:
			ab = AbstractRetrieval(doi)
			if ab.authors:
				for author in ab.authors:
					authors_set.add(author.auid)

		except Exception as e:
			logging.error('DOI {} raised the following errors'.format(doi))
			logging.error('{}'.format(e))
	print("Completed gathering author ids for {} DOIs".format(len(dois)))
	print("Saving the pickle file...")
	pickle_file = open(file.split(".csv")[0] +'.pkl', 'wb')
	pickle.dump(authors_set, pickle_file)
	pickle_file.close()
	print("Pickle file saved")

	print("Processing author ids...")
	for auid in tqdm(list(authors_set)):
		
		try:
			au = AuthorRetrieval(auid)
			author_id = auid
			# List of named tuples
			current_affiliation = au.affiliation_current[0]

			institution_id = current_affiliation.id
			institution_name = current_affiliation.preferred_name
			
			# If needed
			name_variants = au.name_variants


			subject_areas = au.subject_areas
			areas = []
			if subject_areas:
				for subject in subject_areas:
					areas.append(subject.area)
				areas_string = ', '.join(areas)
			else:
				areas_string = ''

			# Excludes the book chapters and notes
			document_count = au.document_count

			# Rest of data attributes
			given_name = au.given_name
			surname = au.surname
			h_index = au.h_index
			citation_count = au.citation_count
			cited_by_count = au.cited_by_count
			author_orcid = au.orcid
			publication_range = au.publication_range
			awards_won = 0

			past_affiliation_list = au.affiliation_history
			if past_affiliation_list:
				for pa in past_affiliation_list:
					author_rows.append([author_id, author_orcid, pa.id, pa.preferred_name])

			rows.append([author_id, author_orcid, given_name, surname, institution_id, institution_name, awards_won, h_index, citation_count, cited_by_count, publication_range, areas_string])
		except Exception as e:
			logging.error('Author ID {} raised the following errors'.format(auid))
			logging.error('{}'.format(e))
			pickle_file = open(file.split(".csv")[0] +'_authors.pkl', 'wb')
			pickle.dump([rows,author_rows], pickle_file)
			pickle_file.close()

	# print(rows)	
	authors_df = pd.DataFrame(rows, columns = columns)
	authors_aff_df = pd.DataFrame(author_rows, columns = author_columns)

	authors_df.to_csv(authors_path+file)
	authors_aff_df.to_csv(authors_path+'Author_affiliation_history/'+file)



for journal in journals:
	# print(journal)
	process_journal(journal)
	exit()

