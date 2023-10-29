import requests
from bs4 import BeautifulSoup
import urllib
import re
import time
import numpy as np
import pandas as pd

def get_bib(id, title, author, year, doi=""):
    template = '''@article{{ref__id__,
        author = {__author__},
        title = {__title__},
        year = {__year__},
        doi = {__doi__}
    }}
    '''
    template = template.replace("__id__", id)
    template = template.replace("__author__", author)
    template = template.replace("__title__", title)
    template = template.replace("__year__", year)
    template = template.replace("__doi__", doi)
    return template 
    
def extract_field_from_bibtex(field, bibtex_text):
    # Define a regular expression to match the title field in BibTeX
    title_regex = r''+field+'\s*=\s*{([^{}]+)}'

    # Find all matches of the title regex in the input text
    title_matches = re.findall(title_regex, bibtex_text)

    # Remove leading and trailing spaces from the titles and return them as a list
    titles = [title.strip() for title in title_matches]

    return titles



def get_google_scholar_urls(title):
    search_query = title
    # Encode the search query
    encoded_query = urllib.parse.quote(search_query)
    search_url = f"https://scholar.google.com/scholar?q={encoded_query}"

    return search_url
## don't do this as google blocks you
    # # Send a GET request to Google Scholar
    # # Define headers to mimic a Firefox request
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    # }
    # response = requests.get(search_url, headers)
    # if response.status_code != 200:
    #     print("Bad response", response.status_code)
    #     # print(response)
    # # Parse the search results page
    # s = BeautifulSoup(response.text, 'html.parser')
    # links = s.find_all('a')
    # good_links = []
    # for a in s.find_all('a'):
    #     if (a.attrs['href'].startswith('https')) and (a.attrs['href'].startswith('https://accounts.') is False):
    #         #  print(a.attrs['href'])
    #          good_links.append(a.attrs['href'])
    
    # return good_links

# Example usage:

with open('../data/final_pub_list_no_urls.bib', 'r') as f:
    data = f.read()

fields = ["author", "title", "year"]
data_d = {}
for f in fields:
    data_d[f] = extract_field_from_bibtex(f, data)
# titles = extract_titles_from_bibtex(data)
# authors = extract_authors_from_bibtex(data)
# assert (len(data_d['title']) == len(data_d['author']))
# print(titles)
urls = []
for i in range(len(data_d['title'])):
    title = data_d['title'][i]
    # author = data_d['author'][i]
    # year = data_d['year'][i]
    scholar_search_url = get_google_scholar_urls(title)
    urls.append(scholar_search_url)

df = pd.DataFrame({'title':data_d['title'], 'url':urls})
df.to_csv('gitdata.csv')



    