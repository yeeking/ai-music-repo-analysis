# step 10 read the CSV labels file
# and add it as a column to the main file

import pandas as pd 

dfile = 'data/main-data-with-labels-all.csv'
lfile = 'data/gpt-labels.csv'
df = pd.read_csv(dfile)
labs = pd.read_csv(lfile)
labels = []
for ind,row in df.iterrows():
    repo = row["Repository"]
    if pd.notna(repo):
        repo = repo.split('/')[1]
        # print(repo)
        lsub = labs[labs["Subfolder"] == repo]
        if len(lsub) == 0:
            type_label = ""
            print(repo)
        else:
            type_label = lsub.iloc[0][1]
            # print(repo, type_label)
    else:
        # no repo
        type_label = ""
    labels.append(type_label)

df['Type'] = labels
df.to_csv('data/main-data-chat-labels.csv')
