import json
from urllib.request import urlopen
import ssl
from os import listdir
from os.path import isfile, join
import pandas as pd
import unicodedata

ssl._create_default_https_context = ssl._create_unverified_context
myKey = "fmtmgHwCVbzXroqmVU"
url = "https://gender-api.com/get?key=" + myKey + "&name=kevin"
response = urlopen(url)
decoded = response.read().decode('utf-8')
data = json.loads(decoded)
print( "Gender: " + data["gender"]) #Gender: male



journals_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Journals_data/'
authors_path = '/Users/shubhamgondane/volunteer_work/data/article_journals_data/Authors_data/'
journals = [f for f in listdir(journals_path) if isfile(join(journals_path, f)) and f not in ['.DS_Store']]

# for journal in journals:
# 	df = pd.read_csv(journals_path+journal, encoding='utf-8')
# 	name_df = df[['author_given','author_family']]
# 	new = name_df["author_given"].str.split(" ", n = 1, expand = True) 
# 	name_df["First Name"]= new[0] 
# 	name_df["Middle Name"]= new[1]

# 	name_df.to_csv(journals_path+'Journal_with_gender/Input/'+journal+'_gender.csv', encoding='utf-8')


journal = 'Comparative Education Review.csv'
df = pd.read_csv(journals_path+journal, encoding='utf-8')
name_df = df[['author_given','author_family']]
name_df['author_given'] =  name_df['author_given'].str.split().str.join(' ')
new = name_df["author_given"].str.split(" ", n = 1, expand = True) 
name_df["First Name"] = new[0] 
name_df["Middle Name"]= new[1]
print(name_df["First Name"].values.tolist())
name_df.to_csv(journals_path+'Journal_with_gender/Input/'+journal+'_gender.csv', encoding='utf-8')