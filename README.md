# ai-music-repo-analysis
Code and data relating to a research paper analysing github repos for AI-music software.

The paper involved the following steps:

* gathering a list of 600 AI-music related research papers (by parsing / copying refs from four review papers)
* preparing the final ref list as bibtex with valid paper titles -> data/final_pub_list_no_urls.bib
* searching on Google scholar for each paper and saving the scholar page as HTML: 
  1-bibtex-to-google-scholar-search-urls.py and 2-scholar-search-to-paper-url.js
 (without getting banned :) )

* extracting PDF urls for the papers from the scholar pages (and other stats) 

* adding the paper URLs back into the bibtex file: 4-zotero-export-to-git-links.py

* importing the bibtex with urls as DOIs into zotero

* Using zotero's PDF finding function to get PDFs from DOI urls

* Extracting text from all PDFs and finding github links

* Gather stats for github repos from github API: 5-get-github-api-info.py
* Cloning github repos
