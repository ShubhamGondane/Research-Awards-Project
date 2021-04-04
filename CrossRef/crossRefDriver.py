from habanero import Crossref
import pandas as pd
from collections import defaultdict
from tqdm import tqdm 
import string

cr = Crossref()
input_file = "~/volunteer_work/data/Article_Awards.csv"

def getEmptyLists(n):
	return ["" for _ in range(n)]

def getJSONFromAPI(query):
	x = cr.works(query = query)
	return x["message"]["items"][0]

def getArticleInfo(input_file):
	article_titles = set()
	df = pd.read_csv(input_file, encoding="utf-8")
	titles = df['Article Title'].values.tolist()
	edge_case = [" ", "", "No award made", "No Award Given"," No Award Given"]

	for title in titles:
		if title not in edge_case:
			article_titles.add(title)

	article_titles = list({x for x in article_titles if pd.notna(x)})
	article_titles.sort()

	article_info_mapping = defaultdict(list)

	for title in tqdm(article_titles, desc="Calling the API"):
		
		# Clean the title 
		split = title.strip()
		translator = str.maketrans('', '', string.punctuation)
		title_text = split.translate(translator)

		item = getJSONFromAPI(title_text)
		# Get article metadata
		keys_to_search =["publisher", "volume", "issue", "page"]

		for k in keys_to_search:
			if k in item.keys():
				article_info_mapping[title].append(item[k])
			else:
				article_info_mapping[title].append("")
		
		# Get authors and affliation
		if "author" in item.keys():
			authors_list = item["author"]
			for author_item in authors_list:
				# Construct the name
				authorName = ""
				if "given" in author_item.keys():
					authorName += author_item["given"]
				if "family" in author_item.keys():
					authorName += author_item["family"]

				# Get the affiliation
				affiliation = ""
				if "affiliation" in author_item.keys():
					if len(author_item["affiliation"]) > 0:
						affiliation = author_item["affiliation"][0]["name"]

				article_info_mapping[title].append([authorName,affiliation])
		# print(article_info_mapping)	

	# print(article_info_mapping)
	# Add columns 
	n = len(titles)
	publisher_list, volume_list, issue_list, page_list = getEmptyLists(n), getEmptyLists(n), getEmptyLists(n), getEmptyLists(n)
	author_names_list, affiliation_list = getEmptyLists(n), getEmptyLists(n)
	
	# Keep track of duplicate titles
	not_seen = {x:True for x in titles}
	i = 0
	flag = False
	while i < len(titles): 
		flag = False
		if titles[i] in article_info_mapping and not_seen[titles[i]]:
			p = article_info_mapping[titles[i]]
			not_seen[titles[i]] = False
			for authors in p[4:]:
				author_names_list[i] = authors[0]
				affiliation_list[i] = authors[1]
				publisher_list[i] = p[0]
				volume_list[i] = p[1]
				issue_list[i] = p[2]
				page_list[i] = p[3]
				i += 1
				flag = True
		if not flag:	
			i += 1
		else:
			continue
			


	df["Updated Names"] = author_names_list
	df["New Affiliation"] = affiliation_list
	df["Journal"] = publisher_list
	df["Volume"] = volume_list
	df["Issue"] = issue_list
	df["Page"] = page_list

	return df

output_df = getArticleInfo(input_file)
output_df.to_csv("~/volunteer_work/data/Article_Awards1.csv", encoding="utf-8")

