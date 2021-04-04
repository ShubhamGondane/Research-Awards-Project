from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from tqdm import tqdm 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import random

url ='https://journals.sagepub.com/doi/full/10.3102/0002831212471417'
sage_base_url = 'https://journals.sagepub.com/doi/full/'
altmetric_base_url = 'https://sage.altmetric.com/details/'

# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0")

opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)

def get_altmetric_url(url):
	altmetric_number = None
	altmetric_link = None
	try:
		browser.get(url)
		time.sleep(random.randint(2, 3))

		altmetric_container = browser.find_element_by_class_name("content")
		# print(altmetric_container)
		img_src = altmetric_container.find_elements_by_tag_name('img')
		
		# There are two images here in this tag. We need the first one.
		altmetric_number = int(img_src[0].get_attribute('alt').split(" ")[-1])
		if altmetric_number > 0:
			# Only go here if score > 0
			link = altmetric_container.find_elements_by_tag_name('a')
			altmetric_link = link[0].get_attribute('href')

		# print(altmetric_number)
		# print(altmetric_link)

		
		
	except NoSuchElementException as e:
		print("NoSuchElementException")
		
	finally:
		return altmetric_number, altmetric_link
		# browser.close()

def get_altmetric_data(link):
	rows = []
	try:
		browser.get(link)
		time.sleep(random.randint(2, 4))
		post_list = browser.find_element_by_class_name("post-list")
		posts = post_list.find_elements_by_tag_name('article')
		
		for post in posts:
			# print(post)
			entire_text = post.text
			lines = entire_text.split("\n")
			rows.append(lines)

	except NoSuchElementException as e:
		print("NoSuchElementException")
		
	finally:
		return rows

		

# get_altmetric_url(url)
# link = 'https://www.altmetric.com/details.php?domain=journals.sagepub.com&citation_id=1317598'
# citation_id = link.split("=")[-1]
# altmetric_url = altmetric_base_url + citation_id + '/twitter'
# print(citation_id)
# tweets = get_altmetric_data(altmetric_url)
# print(tweets)

file = 'Journal of Educational and Behavioral Statistics_1'
base_file_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Journals_data/'+file+'.csv'
output_file_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Twitter_data/JournalofEducationalandBehavioralStatistics/'+file
def process_journal(file):
	df = pd.read_csv(file, encoding='utf-8')
	Dois = df['DOI'].values.tolist()
	Dois = list(set(Dois))
	rows = []
	i = 1
	start = 0
	columns = ['Name', 'Twitter_handle', 'Tweet_text', 'Date', 'DOI']
	prev = 50
	for doi in tqdm(Dois[start:]):
		doi = str(doi)
		print("Processing {} DOI out of {}...".format(i, len(Dois)))
		altmetric_number, altmetric_link = get_altmetric_url(sage_base_url+doi)
		if altmetric_link:
			citation_id = altmetric_link.split("=")[-1]
			altmetric_url = altmetric_base_url + citation_id + '/twitter'
			tweets = get_altmetric_data(altmetric_url)
			for tweet in tweets:
				if len(tweet) != 0:
					rows.append(tweet+[doi])
		i += 1


		if len(rows) > prev: 
			write_df = pd.DataFrame(rows, columns=columns)
			prev += 50
			write_df.to_csv(output_file_path+'_tweets_'+str(prev)+'.csv',encoding='utf-8')

	write_df = pd.DataFrame(rows, columns=columns)
	write_df.to_csv(output_file_path+'_tweets_'+str(prev)+'.csv',encoding='utf-8')
	browser.close()


process_journal(base_file_path)









