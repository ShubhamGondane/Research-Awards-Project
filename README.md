# Research-Awards-Project

## CrossRef is for collecting information on articles
#### 1. crossRefJournal.py for getting the journal data from CrossRef
#### https://www.crossref.org
#### Python module - https://github.com/sckott/habanero
#### 
#### 2. crossRefClean.py for cleaning the data collected
####

## Elsevier is for collecting information on authors
#### 1. get_author_data.py for getting information on the article authors
#### https://www.scopus.com/home.uri
#### Python module - https://pybliometrics.readthedocs.io/en/stable/
#### 2. web_crawler.py for getting altmetric data (Tweets) for articles

## genderAPI is for collecting gender information on authors
#### 1. create_gender_input_files.py is for collecting information on book authors
#### https://gender-api.com/
#### 2. genderAPIDriver.py is for collecting information on article authors

## googleBooks is for collecting information about books
#### 1. googlebooksDriver.py is for colleting information about the books that won the awards 
#### https://developers.google.com/books
#### 2. googlebookDriverPublisher.py for collecting information about the publishers we saved from the previous file

## googleScholar is for collecting information about authors
#### 1. driver_articles.py is for colleting the article author information 
#### https://scholar.google.com
#### Python module - https://github.com/scholarly-python-package/scholarly
#### 2. driver_v1.py is for colleting the book author information

## race is for collecting information about race
#### Python module - https://github.com/appeler/ethnicolr
#### 1. driver.py is for colleting the author race information for books as well as authors
