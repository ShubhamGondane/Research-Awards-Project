from habanero import Crossref
import pandas as pd
from collections import defaultdict
from tqdm import tqdm 
import json
import csv
from nested_dict_to_csv import main
cr = Crossref()

journals = ["American Educational Research Journal", "Educational Evaluation and Policy Analysis", "Educational Researcher", "Journal of Educational and Behavioral Statistics", "Comparative Education Review", "Educational Administration Quarterly","Journal of Research on Leadership Education"]
base_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/'

def getRelevantArticles(journal):
	filters = {
		'from_pub_date':'2000',
		'until_pub_date':'2020',
		'container_title':journal,
	}
	articles = cr.works(query=journal, filter=filters, limit=1000)
	total_results = articles["message"]["total-results"]
	results = articles["message"]["items"]
	if total_results <= 1000:
		return results
	else:
		articles = cr.works(query=journal, filter=filters, offset = 1000, limit=1000)
		print(articles["message"]["total-results"])
		return results + articles["message"]["items"]

def get_leaves(item, key=None, key_prefix=""):
	"""
	This function converts nested dictionary structure to flat
	"""
	if isinstance(item, dict):
		leaves = {}
		"""Iterates the dictionary and go to leaf node after that calls to get_leaves function recursively to go to leaves level"""
		for item_key in item.keys():
			"""Some times leaves and parents or some other leaves might have same key that's why adding leave node key to distinguish"""
			temp_key_prefix = (
				item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
			)
			leaves.update(get_leaves(item[item_key], item_key, temp_key_prefix))
		return leaves
	elif isinstance(item, list):
		leaves = {}
		elements = []
		"""Iterates the list and go to leaf node after that if it is leave then simply add value to current key's list or 
		calls to get_leaves function recursively to go to leaves level"""
		for element in item:
			if isinstance(element, dict) or isinstance(element, list):
				leaves.update(get_leaves(element, key, key_prefix))
			else:
				elements.append(element)
		if len(elements) > 0:
			leaves[key] = elements
		return leaves
	else:
		return {key_prefix: item}

def writeToCSV(json_records, journal):
	if not json_records:
		return
	print("Writing {} items to file".format(len(json_records)))
	output_file_path = base_path + journal + '.csv'
	df_path = base_path + journal + 'df.csv'
	fieldnames = set()
	for record in json_records:
		fieldnames.update(set(get_leaves(record).keys()))
	
	rows = []
	with open(output_file_path, "w", newline="") as f_output:
		csv_output = csv.DictWriter(f_output, delimiter=",", fieldnames=sorted(fieldnames))
		csv_output.writeheader()
		csv_output.writerows(get_leaves(entry) for entry in json_records)
		
		# rows.append(get_leaves(entry).values() for entry in json_records)

	# df = pd.DataFrame(rows, columns=list(fieldnames))
	# df.to_csv(df_path, encoding='utf-8')

def write_to_csv(json_records, journal):
	if not json_records:
		return
	
	# indexed and created are two fields created by crossref. The original publish date is published-date.
	titles = ["date-time", "timestamp", "reference-count", "publisher", "issue", "journal", "published-date", "DOI" ,"created_date-time", "created_timestamp", "pages", 
	"title", "volume" ,"URL", "subject", "author", "affiliation"]
	
	rows = []
	for i, record in enumerate(json_records):
		print("Processing {}th record out of {}".format(i+1, len(json_records)))
		record_details = []
		if "indexed" in record.keys():
			if "date-time" in record["indexed"].keys():
				record_details.append(record["indexed"]["date-time"])

			if "timestamp" in record["indexed"].keys():
				record_details.append(record["indexed"]["timestamp"])

		if "reference-count" in record.keys():
			record_details.append(record["reference-count"])

		if "publisher" in record.keys():
			record_details.append(record["publisher"])

		if "issue" in record.keys():
			record_details.append(record["issue"])
		else:
			# Only for the case of Journal of Research on Leadership Education. There is no issue number in the JSON data
			record_details.append("")

		if "short-container-title" in record.keys():
			if len(record["short-container-title"]) != 0:
				record_details.append(record["short-container-title"][0])


		if "published-print" in record.keys():
			if "date-parts" in record["published-print"].keys():
				for parts in record["published-print"]["date-parts"]:
					record_details.append("-".join([str(p) for p in parts[::-1]]))
		else:
			# Only for the case of Journal of Research on Leadership Education. There is no issue number in the JSON data
			record_details.append("")

		if "DOI" in record.keys():
			record_details.append(record["DOI"])

		if "created" in record.keys():
			if "date-time" in record["indexed"].keys():
				record_details.append(record["indexed"]["date-time"])

			if "timestamp" in record["indexed"].keys():
				record_details.append(record["indexed"]["timestamp"])

		if "page" in record.keys():
			record_details.append(record["page"])

		if "title" in record.keys():
			record_details.append(record["title"][0])

		if "volume" in record.keys():
			record_details.append(record["volume"])
		else:
			# Only for the case of Journal of Research on Leadership Education. There is no issue number in the JSON data
			record_details.append("")

		authors = []
		if "author" in record.keys():
			for author_record in record["author"]:
				author_name = ""
				if "given" in author_record.keys() and "family" in author_record.keys():
					author_name = author_record["given"] + " " +author_record["family"]

				author_affiliation = ""
				if len(author_record["affiliation"]) != 0:
					author_affiliation = author_record["affiliation"][0]["name"]
				authors.append([author_name, author_affiliation])

		if "URL" in record.keys():
			record_details.append(record["URL"])

		if "subject" in record.keys():
			record_details.append(record["subject"][0])
		else:
			# Only for the case of Journal of Research on Leadership Education. There is no issue number in the JSON data
			record_details.append("")

		for a in authors:
			rows.append(record_details + a)
	
	df = pd.DataFrame(rows, columns=titles)
	print(df.shape)
	print("Writing {} items to file".format(df.shape[0]))
	output_file_path = base_path + journal + '.csv'
	df.to_csv(output_file_path, encoding='utf-8')



for journal in tqdm(journals[-1:], desc = "Getting articles for "):
	print(journal)
	json_records = getRelevantArticles(journal)
	write_to_csv(json_records, journal)
	













