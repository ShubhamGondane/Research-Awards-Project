import pandas as pd
from os import listdir
from os.path import isfile, join
from ethnicolr import census_ln, pred_census_ln, pred_wiki_name

names = [{'first name': 'jane', 'last name': 'smith'},
{'first name': 'jeongeun', 'last name': 'kim'},
{'first name': 'shubham', 'last name': 'gondane'},
{'first name': 'john', 'last name': 'jackson'}]

df = pd.DataFrame(names)

result = pred_wiki_name(df, 'last name', 'first name')
print(result.columns)

result = pred_census_ln(df, 'last name', 2010)
print(result.columns)



input_folder = '~/volunteer_work/data/book_publishers_data/authors_data/Gender_output/'
output_folder = '~/volunteer_work/data/book_publishers_data/authors_data/Race/'

input_files = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and f != '.DS_Store']

for file in input_files:
	df = pd.read_csv(input_folder+file)
	new = df["Author_name"].str.split(" ", n=1, expand = True)
	df["last_name"] = new[1]

	wiki_result = pred_wiki_name(df, 'last_name','first_name')
	wiki_result.drop(columns=['Asian,GreaterEastAsian,EastAsian',
       'Asian,GreaterEastAsian,Japanese', 'Asian,IndianSubContinent',
       'GreaterAfrican,Africans', 'GreaterAfrican,Muslim',
       'GreaterEuropean,British', 'GreaterEuropean,EastEuropean',
       'GreaterEuropean,Jewish', 'GreaterEuropean,WestEuropean,French',
       'GreaterEuropean,WestEuropean,Germanic',
       'GreaterEuropean,WestEuropean,Hispanic',
       'GreaterEuropean,WestEuropean,Italian',
       'GreaterEuropean,WestEuropean,Nordic'], inplace=True)
	wiki_result = wiki_result.rename(columns={'race': 'wiki_race'})

	census_result = pred_census_ln(wiki_result, 'last_name', 2010)

	census_result = census_result.rename(columns={'race': 'census_race'})
	census_result.to_csv(output_folder+file)
	
