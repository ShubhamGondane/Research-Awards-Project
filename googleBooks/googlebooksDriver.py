import googlebooks
import pandas as pd
from collections import defaultdict
from tqdm import tqdm 
from time import sleep
from fuzzywuzzy import fuzz
import string
'''
https://developers.google.com/books/docs/v1/reference/volumes/list?apix=true&apix_params=%7B%22maxResults%22%3A5%2C%22orderBy%22%3A%22relevance%22%2C%22q%22%3A%22Equity%20and%20Excellence%20in%20American%20Higher%20Education%22%7D
'''
api = googlebooks.Api()
input_file = "/Users/shubhamgondane/volunteer_work/data/Book_Awards.csv"
api_key = "AIzaSyCxutnfKcPnm6iQWFHowebW6RWvIM5Av7A"

def getJSONFromAPIUsingPrefix(query, prefix=True):
	json_data = api.list(q=query, maxResults=5, orderBy="relevance")
	if json_data:
		print("Found it")
		return json_data['items'][0]


# Test
'''
query = "Between Citizens and the State The Politics of American Higher Education in the Twentieth Century Princeton University Press 2012"
temp = "'q:" + query + "'"
print(temp)
json_data = getJSONFromAPIUsingPrefix(api, query)
for item in json_data:
	print(item['volumeInfo']['title'])

# print(json_data)
exit()
'''
def getBookInfo(api, input_file):
	# To store unique book titles
	book_titles = set()
	books_metadata = []
	# Input file read
	df = pd.read_csv(input_file)
	titles = df['Book Title'].values.tolist()
	authors = df['Author'].values.tolist()

	# Cases where no data is available
	edge_case = [" ", "", "No award made", "No Award Given"]

	# Add titles to the set
	for title, author in zip(titles, authors):
		if title not in edge_case:
	
	book_titles = list({x for x in book_titles if pd.notna(x)})
	book_titles.sort()
	not_done = []

	# A dict to keep track of titles and the relevant metadata
	book_author_mapping = defaultdict(list)
	for title in tqdm(book_titles, desc="Calling the API"):
		
		# Clean the title 
		split = title.strip()
		translator = str.maketrans('', '', string.punctuation)
		title_text = split.translate(translator)
		
		
		print(title_text)
		
		# Call to the API
		item = getJSONFromAPIUsingPrefix(title_text)
		if item:
			publisher, publish_year = "",""
			if 'publisher' in item['volumeInfo'].keys():
				publisher = item['volumeInfo']['publisher']
			
			if 'publishedDate' in item['volumeInfo'].keys():
				publish_year = item['volumeInfo']['publishedDate'].split("-")[0]

			book_author_mapping[title].append(publisher)
			book_author_mapping[title].append(publish_year)
			books_metadata.append(item)
		
		if title not in book_author_mapping:
			not_done.append(title)
		

	publisher_list = []
	publish_year_list = []

	for title in tqdm(titles, desc="Processing title "):
		print(title)
		if title in book_author_mapping:
			p = book_author_mapping[title]
			publisher_list.append(p[0])
			publish_year_list.append(p[1])
		else:
			publisher_list.append("")
			publish_year_list.append("")

	# print(book_author_mapping)
	
	# print(not_done)
	df['Publish Year'] = publish_year_list
	df['Publisher'] = publisher_list


	# print(df)
	return df

output_df = getBookInfo(api, input_file)
output_df.to_csv("/Users/shubhamgondane/volunteer_work/data/Book_Awards1.csv")




