#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 20:57:07 2022

@author: marinedjaffardjy
"""

import json
import pandas as pd
import numpy as np
from simil_process import *

#This script makes, for all specified metrics :
#- scores matrices
#- similarity groups
#- similarity dataframes and json
#- similarity dataframes and json grouped

time0=time.time()
#######IMPORTING FILES###########

#snakemake rules
with open('/home/marinedjaffardjy/Documents/Code/Investigating_reuse/json/snk_rule_info_tool.json') as f:
    snk_proc = json.load(f)
#nf proc
with open('/home/marinedjaffardjy/Documents/Code/Similarite_process/json/nf_proc_tool.json') as f:
    nf_proc = json.load(f)

def importing_json_files(file_wf):
    f_wf = open(file_wf) #informations for nf
    # returns JSON object as
    # a dictionary
    wf = json.load(f_wf)
    f_wf.close
    return wf

#importing the wf and auth dict (github info)
dict_nf = importing_json_files('../json/wf_new_crawl_nextflow.json')
auth_nf = importing_json_files('../json/author_clem_nf.json')
dict_snk = importing_json_files('../json/wf_crawl_snakemake.json')
auth_snk = importing_json_files('../json/author_clem_snk.json')

##### WHERE THE JSON OF THE SCORES ARE ##############

scores_nf_lev="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools"
scores_snk_lev="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_snk_tools"
scores_nf_ngram="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/ngram_nf_tools"
scores_snk_ngram="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/ngram_snk_tools"


##### WHERE WE WANT TO SAVE THE MATRICES ##############
    
path_matrix_nf_lev="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/matrix_nf_levenshtein"
path_matrix_snk_lev="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/matrix_snk_levenshtein"
path_matrix_nf_ngram="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/matrix_nf_ngram"
path_matrix_snk_ngram="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/matrix_snk_ngram"


##################PIPELINE########################"

## STEP 1 : MAKING THE SCORE MATRICES
#print(" MAKING THE SCORE MATRICES" )
#
#print("Nextflow :")
#print("levenshtein")
#mat_nf_lev = make_score_matrices(9652,path_matrix_nf_lev,scores_nf_lev,"levenshtein_nf_tools_","levenshtein")
#print("ngram")
#mat_nf_ngram = make_score_matrices(9652,path_matrix_nf_ngram,scores_nf_ngram,"ngram_3_nf_tools_","ngram")
#
#print("Snakemake :")
#print("levenshtein")
#mat_snk_lev = make_score_matrices(5001,path_matrix_snk_lev,scores_snk_lev,"levenshtein_snk_tools_","levenshtein")
#print("ngram")
#mat_snk_ngram = make_score_matrices(5001,path_matrix_snk_ngram,scores_snk_ngram,"ngram_3_snk_tools_","ngram")
#
#print("temps écoulé "+str(time.time()-time0))

## ALTERNATIVE : LISTE DES FICHIERS DE MATRICE
#
#mat_nf_lev = get_matrix_files(path_matrix_nf_lev,9652)
#mat_nf_ngram = get_matrix_files(path_matrix_nf_ngram,9652)
#mat_snk_lev = get_matrix_files(path_matrix_snk_lev,5001)
#mat_snk_ngram = get_matrix_files(path_matrix_snk_ngram,5001)
#
## STEP 2 : MAKING THE GROUPS
#
#print(" MAKING THE GROUPS" )
#
#print("Nextflow :")
#print("levenshtein")
#groups_nf_lev,groups_nf_lev_index=grouping_simple(mat_nf_lev,nf_proc)
#
#filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_nf_lev.json"
#with open(filename,"w") as f:
#    json.dump(groups_nf_lev,f)
#    print(filename)
#    
#print("ngram")
#groups_nf_ngram,groups_nf_ngram_index=grouping_simple(mat_nf_ngram,nf_proc)
#
#filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_nf_ngram.json"
#with open(filename,"w") as f:
#    json.dump(groups_nf_ngram,f)
#    print(filename)
#    
#print("Snakemake :")
#print("levenshtein")
#groups_snk_lev,groups_snk_lev_index=grouping_simple(mat_snk_lev,snk_proc)
#
#filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_snk_lev.json"
#with open(filename,"w") as f:
#    json.dump(groups_snk_lev,f)
#    print(filename)
#    
#print("ngram")
#groups_snk_ngram,groups_snk_ngram_index=grouping_simple(mat_snk_ngram,snk_proc)
#
#filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_snk_ngram.json"
#with open(filename,"w") as f:
#    json.dump(groups_snk_ngram,f)
#    print(filename)
#
#filenames = ["/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_nf_lev.json",
#             "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_nf_ngram.json",
#             "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_snk_lev.json",
#             "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/group_snk_ngram.json"]
#
#print("temps écoulé "+str(time.time()-time0))

# ALTERNATIVE

# STEP 3 : MAKING THE DATAFRAMES

print(" MAKING THE DATAFRAMES" )

print("Nextflow :")
print("levenshtein")

nf_lev_json, nf_lev_df = sim_to_df(groups_nf_lev,dict_nf,"nf")
df_nf_lev = grouping_sim_df(nf_lev_df,len(nf_lev_json),dict_nf)
df_lev_nf_wf = grouping_sim_df_wf(nf_lev_df,len(nf_lev_json),dict_nf,auth_nf)

filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/sim_nf_lev.json"
filename1 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_nf_lev.csv"
filename2 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_nf_lev_wf.csv"

with open(filename,"w") as f:
    json.dump(nf_lev_json,f)
    print(filename)
df_nf_lev.to_csv(filename1)
df_lev_nf_wf.to_csv(filename2)

    
print("ngram")

nf_ngram_json, nf_ngram_df = sim_to_df(groups_nf_ngram,dict_nf,"nf")
df_nf_ngram = grouping_sim_df(nf_ngram_df,len(nf_ngram_json),dict_nf)
df_ngram_nf_wf = grouping_sim_df_wf(nf_ngram_df,len(nf_ngram_json),dict_nf,auth_nf)

filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/sim_nf_ngram.json"
filename1 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_nf_ngram.csv"
filename2 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_nf_ngram_wf.csv"

with open(filename,"w") as f:
    json.dump(nf_ngram_json,f)
    print(filename)
df_nf_ngram.to_csv(filename1)
df_ngram_nf_wf.to_csv(filename2)
    
print("Snakemake :")
print("levenshtein")

snk_lev_json, snk_lev_df = sim_to_df(groups_snk_lev,dict_snk,"snk")
df_snk_lev = grouping_sim_df(snk_lev_df,len(snk_lev_json),dict_snk)
df_lev_snk_wf = grouping_sim_df_wf(snk_lev_df,len(snk_lev_json),dict_snk,auth_snk)

filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/sim_snk_lev.json"
filename1 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_snk_lev.csv"
filename2 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_snk_lev_wf.csv"

with open(filename,"w") as f:
    json.dump(snk_lev_json,f)
    print(filename)
df_snk_lev.to_csv(filename1)
df_lev_snk_wf.to_csv(filename2)

    
print("ngram")

snk_ngram_json, snk_ngram_df = sim_to_df(groups_snk_ngram,dict_snk,"snk")
df_snk_ngram = grouping_sim_df(snk_ngram_df,len(snk_ngram_json),dict_snk)
df_ngram_snk_wf = grouping_sim_df_wf(snk_ngram_df,len(snk_ngram_json),dict_snk,auth_snk)

filename = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/sim_snk_ngram.json"
filename1 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_snk_ngram.csv"
filename2 = "/home/marinedjaffardjy/Documents/Code/Similarite_process/csv/sim_snk_ngram_wf.csv"

with open(filename,"w") as f:
    json.dump(snk_ngram_json,f)
    print(filename)
df_snk_ngram.to_csv(filename1)
df_ngram_snk_wf.to_csv(filename2)













