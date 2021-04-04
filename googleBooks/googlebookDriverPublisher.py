import googlebooks, json, time, string
import pandas as pd
from collections import defaultdict
from tqdm import tqdm 


api = googlebooks.Api()
input_file = "/Users/shubhamgondane/volunteer_work/data/Book_Awards.csv"
# api_key = "AIzaSyCxutnfKcPnm6iQWFHowebW6RWvIM5Av7A"
log_file = open("/Users/shubhamgondane/volunteer_work/src/logging_google_books.txt","w")

def readFromCSV(input_file):
	'''
	Input: String - Path of the CSV file containing list of publishers
	Returns a set of publishers
	'''
	df = pd.read_csv(input_file, encoding='utf-8')
	return set(df['Publishers'].values.tolist())

def runAPIOnPublisher(publisher):
	'''
	Input: String publisher name
	Returns a list of relevant JSON items
	'''
	query = "inpublisher:" + str(publisher)
	json_items_list = []
	start_index = 0
	# try:
	json_data = api.list(q=query)
	total_items = json_data["totalItems"]
	print("Found " + str(total_items) + " total items")
	while start_index < total_items:

		json_data = api.list(q=query, startIndex=start_index, maxResults=40)
		if "items" in json_data.keys():
			for item in json_data["items"]:
				if 'publishedDate' in item['volumeInfo'].keys():
					date = item['volumeInfo']['publishedDate']
					if "-" in date:
						date = date.split("-")[0]
					if "?" in str(date) and date[0] == "2":
						date = "2000"
					if len(date) < 5 and "?" not in date and 2000 <= int(date) < 2020:
						json_items_list.append(item['volumeInfo'])
		start_index += 40
			
	# except:
	# 	log_file.write(publisher)
	# 	log_file.write("\n")
	# finally:
	return json_items_list

def writeToCSV(json_items_list, publisher_name):
	'''
	Input: List of json items
	Returns None
	'''
	if not json_items_list:
		return
	base_path = '/Users/shubhamgondane/volunteer_work/data/book_publishers_data/'
	output_file_path = base_path + publisher_name + '.csv'
	print("Writing {} items to file".format(len(json_items_list)))
	pd.read_json(json.dumps(json_items_list)).to_csv(output_file_path)

input_file = "/Users/shubhamgondane/volunteer_work/data/publisher_data.csv"
publishers_list = readFromCSV(input_file)

for publisher in tqdm(publishers_list, desc="Processing Publishers"):
	print(publisher)
	json_data_list = runAPIOnPublisher(publisher)
	print(len(json_data_list))
	writeToCSV(json_data_list, publisher)
	time.sleep(10)

log_file.close()

# json_data = api.list(q="inpublisher:IAP")
# print(json_data['totalItems'])





