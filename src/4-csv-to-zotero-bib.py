## Step 4 is to convert the current CSV data file 
## containing the list of citations into a bib fil
## so it can be imported to zotero so can use zotero's
## paper downloading function to get as many PDFs as possible
## (it has a better hit rate than just wgetting the urls extracted from scholar)
## once imported to zotero, tell it to download papers
## then export the collection with files for step 5


import random
import string

import pandas as pd


# Function to generate random author names
def generate_random_author():
    first_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
    last_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=7))
    return f"{first_name} {last_name}"

# Function to create a bibtex entry from a row in the dataframe
def row_to_bibtex(row):
    entry = "@article{ref"+str(row['paper_id'])+"\n"
    entry += f"\tauthor = {{paper{row['paper_id']}}},\n"
    # entry += f"\ttitle = {{{row['title']}}},\n"
    entry += f"\ttitle = {{paper {row['paper_id']}}},\n"
    entry += f"\turl = {{{row['paper_url']}}}\n"
    entry += "}"
    return entry

# Create bibtex entries for each row

# Read the CSV file
df = pd.read_csv('main-data.csv')
df.head()
bibtex_entries = df.apply(row_to_bibtex, axis=1).tolist()
bibtex_text = '\n\n'.join(bibtex_entries)

with open('zot.bib', 'w') as f:
    f.write(bibtex_text)
