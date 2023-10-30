# Step 7: assign labels to the rows in the spreadsheet

import pandas as pd
import json 
import numpy
import ast

def get_lang_info(json_list, paper_id):
    """
    return the         "Code total" and "Language_percs" fields for
    the object in the json_list with paper_id == paper_id
    """
    for j in json_list:
        if j["paper_id"] == paper_id:
            # print(j)
            # "Code total": 88690, "Language_percs": [0.7250986582478295, 0.25787574698387644, 0.01702559476829406]
            if "Language_percs" in j.keys() and "Code total" in j.keys():
                lang_percs = j["Language_percs"]    
                code_total = j["Code total"]
                return lang_percs, code_total
    return [0], 0

def assign_main_language(langs, percs, num_lines):
    # "Languages": ["Jupyter Notebook", "Python", "Shell"], "Code total": 88690, "Language_percs": [0.7250986582478295, 0.25787574698387644, 0.01702559476829406], "paper_id": 429},
    # percs = [float(l) for l in langs]
    if type(langs) is not list:
        print("Bad langs", langs)
        return 0, 0
    if len(percs) == 0:
        return 0,0 
    max = percs[0]
    max_i = 0
    if len(langs) > 1:
        for i in range(1, len(percs)):
            if percs[i] > max:
                max_i = i
                max = percs[i]
    print(langs, type(percs),  type(num_lines), max_i)
    print(langs[max_i], num_lines * percs[max_i])
    return langs[max_i], num_lines * percs[max_i]

    


with open('temp.json') as f:
    json_obj = json.loads(f.read())

df = pd.read_csv("main-data-7-labels-extra.csv")

# extra_fields = {"Language percs":[], "Code total":[], "Main language":[], "Main language lines":[]}
extra_fields = {"Main language":[], "Main language lines":[]}

for ind,row in df.iterrows():
    paper_id = row["paper_id"]
    
    # lang_percs,lang_total = get_lang_info(json_obj, paper_id)
    # extra_fields["Language percs"].append(lang_percs)
    # extra_fields["Code total"].append(lang_total)

    if type (row["Languages"]) is str:
        languages = ast.literal_eval(row["Languages"])
        
        # main_lang, lines = assign_main_language(languages, lang_percs, lang_total)
        
        main_lang, lines = assign_main_language(languages, ast.literal_eval(row["Language percs"]), 
                                                           row["Code total"])

        extra_fields["Main language"].append(main_lang)
        extra_fields["Main language lines"].append(lines)
    else:
        extra_fields["Main language"].append("")
        extra_fields["Main language lines"].append(0)
    
    
for k in extra_fields.keys():
    df[k] = extra_fields[k]

df.to_csv('main-data-7-labels-all.csv')