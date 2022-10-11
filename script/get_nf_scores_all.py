#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 00:34:50 2022

@author: marinedjaffardjy

"""

import json

path_nf='/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools/levenshtein_nf_tools_'
print(path_nf)

with open('/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools/levenshtein_nf_tools_3800.json') as f1:
    print('a')
    scores = json.load(f1)

print(len(scores))

autres=list(range(3850,9650,50)).append(9651)
print(len(autres))
i=0
for el in autres:
    print(i)
    with open(path_nf+el+'.json') as f1:
        scores_new = json.load(f1)
    scores+=scores_new
    i+=1
    

with open('/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools/levenshtein_nf_tools_all.json','w') as f1:
    json.dump(scores,f1)