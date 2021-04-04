from pybliometrics.scopus import AbstractRetrieval, ScopusSearch, AuthorRetrieval
import pandas as pd
import time
from tqdm import tqdm 
from os import listdir
from os.path import isfile, join

ab = AbstractRetrieval("10.3102/0002831212468787")
# print(ab.title)
# print(ab.authors)
# print(ab.authors[0].auid)
au1 = AuthorRetrieval(ab.authors[0].auid)
print(au1._json)
# import requests
# keys=['df5d031de5ea050915f3cba84cc1e5a0']
# # url = 'https://api.elsevier.com/content/search/scopus?query=KEY%20(10.3102/00028312073129103)&apiKey=' + keys[0]
# url = 'https://api.elsevier.com/content/abstract/doi/{10.3102/0002831207312910}&apiKey=' + keys[0]

# res = requests.request('GET', url)

# print(res)
# # print(res.json())

# fb5b690aa98749a36a40d36d6315cc86