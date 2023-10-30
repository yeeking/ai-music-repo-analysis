# stage 8: dump out the list of git urls for cloning 
# then send to chat gpt for labelling


import pandas as pd

dfile = "data/main-data-with-labels-all.csv"
df = pd.read_csv(dfile)
df_sub = df[df["git_urls"].notna()]
for ind,row in df_sub.iterrows():
    # print(ind, row["git_urls"])
    url = row["git_urls"].split(",")[0]
    if (row["Code total"]) > 0:
        print(url + ".git")


