## Step 3 is to extract useful information from the scholar
## pages for the various papers. 
## e.g. the first link for the paper which is likely to lead to a PDF
## the number of citations

import pandas as pd 
import os 
from bs4 import BeautifulSoup


def get_cite_count(soup:BeautifulSoup):
    # <a href="/scholar?cites=6908439058279720375&amp;as_sdt=2005&amp;sciodt=0,5&amp;hl=en">Cited by 51</a>
    # Extract the number after 'cited by'

    cited_by_element = soup.find(text=lambda x: 'Cited by' in x)
    cited_by_number = None
    # print(cited_by_element)
    if cited_by_element != None:
        citations = int(cited_by_element.split("Cited by ")[1])
        print(citations)
    else:
        citations = 0
    return citations

def get_pdf_link(soup:BeautifulSoup):
# https://www.researchgate.net/profile/Marcelo-Gimenes/publication/318431828_An_Ontomemetic_Approach_to_Musical_Intelligence/links/596912faaca2728ca67c0061/An-Ontomemetic-Approach-to-Musical-Intelligence.pdf
    # Extract the first link that doesn't start with the specified prefixes
    links = soup.find_all('a', href=True)
    valid_link = None
    for link in links:
        href = link['href']
        # best case
        if href.endswith('pdf'):
            return href
        # otherwise - at least return a link
        if (not href.startswith(("https://accounts.", "https://scholar."))) and (href.startswith("https")):
            return href
    print("links", len(links), "no luck :(")
    return ""
    
scholar_dir = "/home/matthewyk/Downloads/"
# scholar_dir = "./"
data_file = "/home/matthewyk/Dropbox/Research/Papers/WIP/2024_Evomusart/ai-music-repo-analysis/data/scholar_urls.csv"
df = pd.read_csv(data_file)
cites = []
paper_urls = []
paper_ids = []
found_pdfs = 0
found_papers = 0
for ind,row in df.iterrows():
    scholar_file = "scholar_"+ str(ind) + '.html'
    # set some defaults to ensure we get a csv
    url = ""
    citations = 0
    if os.path.exists(scholar_dir + scholar_file):
        with open(scholar_dir + scholar_file) as f:
            content = f.read()
            # Parse the file using Beautiful Soup
            soup = BeautifulSoup(content, 'html.parser')
            url = get_pdf_link(soup)
            found_papers = found_papers + 1
            if url.endswith('pdf'):
                found_pdfs = found_pdfs + 1
            citations = get_cite_count(soup)
    paper_ids.append(ind)
    paper_urls.append(url)
    cites.append(citations)

df['paper_id'] = paper_ids
df['citations'] = cites
df['paper_url'] = paper_urls
print("Found direct pdfs", found_pdfs, "of", found_papers)
df.to_csv('main-data-3-sch-links.csv')