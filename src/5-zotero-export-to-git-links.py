## Step 5 is to parse the pdfs exported from zotero
## and to extract any github links
## eventually adding them to the master CSV file

import os
import re
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import pandas as pd 

def get_paper_id(filename = 'paper 10.pdf'):
    filename = filename.split(' ')[1]
    filename = filename.split('.pdf')[0]
    return int(filename)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def extract_github_links_from_content(content):
    # Regular expression pattern to extract links
    # pattern = r'http[^\s,\.]*github[^ \s,\.]*'
    pattern = r'https://github\.com/[\w-]+/[\w-]+(?:\n|(?=\s|[\.,]|$))'
    # pattern = r'https://github\.com/[\w-]+/[\w-]+(?=\s|[\.,]|$)'
    # Find all matches in the text
    matches = re.findall(pattern, content)
    return matches
    # return re.findall(r'https://github.com/[^ ]+', content)

def extract_github_links_from_file(file_path):
    if file_path.endswith('.pdf'):
        content = extract_text_from_pdf(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    return extract_github_links_from_content(content)

def search_github_links_in_directory(directory):
    github_links_results = {}
    all_git_links = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.html', '.pdf')):
                file_path = os.path.join(root, file)
                print("Processing file", file)
                links = extract_github_links_from_file(file_path)
                if links:
                    print("Found", len(links), "github repos")
                    print(links)
                    links = [l.replace('\n', '') for l in links]
                    github_links_results[get_paper_id(file)] = links
                    all_git_links.extend(links)
                    # return github_links_results, all_git_links

    return github_links_results, all_git_links

# Replace with the path to your directory containing the files

directory_path = "/home/matthewyk/Dropbox/Research/Papers/WIP/2024_Evomusart/ai-music-repo-analysis/data/zot2/"

github_links,all_links = search_github_links_in_directory(directory_path)

## add the github links to the main csv file
df = pd.read_csv('main-data-3-sch-links.csv')
# generate zotero export filenames
all_gits = []
for ind, row in df.iterrows():
    paper_id = row["paper_id"]
    # find the metching links for this paper id
    paper_gits = ""
    if paper_id in github_links.keys():
        links = github_links[paper_id]
        paper_gits = ','.join(links)
    all_gits.append(paper_gits)
            
df['git_urls'] = all_gits
df.to_csv('main-data-5-git-links.csv')
# with open('github-links.txt', 'w') as f:
#     for l in all_links:
#         f.write(l.strip() + "\n")
    #
    # print(all_links)
