#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 00:05:02 2022

@author: marinedjaffardjy
"""

### this script computes levenshtein for snk and nf proc with tools
import json
import time
import simil_process
import pandas as pd

################
# DEFINING VARIABLES
################

time0 = time.time()

####### WHERE THE SCORES OF PROC SIMILARITY ARE
 
snk_proc_path = "../json/levenshtein_snk_tools_shell/levenshtein_snk_tools_shell"   
nf_proc_path = "../json/levenshtein_nf_tools_shell/levenshtein_nf_tools_shell"

snk_sim_path = "../json/levenshtein_snk_tools_shell/"   
nf_sim_path = "../json/levenshtein_nf_tools_shell/"


##### WHERE WE WANT TO SAVE THE MATRICES ##############
    
path_matrix_nf_lev="../json/matrix_nf_levenshtein"
path_matrix_snk_lev="../json/matrix_snk_levenshtein"



################
# IMPORTING THE FILES
################

    
with open("../json/source_files/nf_proc_tool_shell.json") as f:
    nf_proc = json.load(f)
    
with open('../json/source_files/snk_proc_tool_shell.json') as f:
    snk_proc = json.load(f)
    
def importing_json_files(file_wf):
    f_wf = open(file_wf) #informations for nf
    # returns JSON object as
    # a dictionary
    wf = json.load(f_wf)
    f_wf.close
    return wf

#importing the wf and auth dict (github info)
dict_nf = importing_json_files('../json/source_files/wf_new_crawl_nextflow.json')
auth_nf = importing_json_files('../json/source_files/author_clem_nf.json')
dict_snk = importing_json_files('../json/source_files/wf_crawl_snakemake.json')
auth_snk = importing_json_files('../json/source_files/author_clem_snk.json')

    
# ################
# # LAUNCHING THE PIPELINE
# ###############

# # STEP 1 : compute levenshtein scores

# print(" COMPUTING SCORES" )

# ##nf tools proc shell
# print("Nextflow :")
# print("levenshtein")
# simil_process.levenshtein_proc_shell(nf_proc,0,nf_proc_path)


# print("total run time "+str(time.time()-time0))

# #snk tools proc shell
# print("Snakemake :")
# print("levenshtein")
# simil_process.levenshtein_proc_shell(snk_proc,0,snk_proc_path)


# print("total run time "+str(time.time()-time0))


# # STEP 2 : make score matrices

# print(" MAKING THE SCORE MATRICES" )

# print("Nextflow :")
# print("levenshtein")
# mat_nf_lev = simil_process.make_score_matrices(len(nf_proc),path_matrix_nf_lev,nf_sim_path,"levenshtein_nf_tools_shell_","levenshtein")

# print("Snakemake :")
# print("levenshtein")
# mat_snk_lev = simil_process.make_score_matrices(len(snk_proc),path_matrix_snk_lev,snk_sim_path,"levenshtein_snk_tools_shell_","levenshtein")

# print("total run time "+str(time.time()-time0))




# Step 3 : make the groups

print(" MAKING THE GROUPS" )

mat_nf_lev = simil_process.get_matrix_files(path_matrix_nf_lev,len(nf_proc))
mat_snk_lev = simil_process.get_matrix_files(path_matrix_snk_lev,len(snk_proc))


print("Nextflow :")
print("levenshtein")
groups_nf_lev , groups_nf_lev_index = simil_process.grouping_simple(mat_nf_lev,nf_proc)

filename = "../json/source_files/results/group_nf_lev.json"
with open(filename,"w") as f:
    json.dump(groups_nf_lev,f)
    print(filename)
    
    
    
print("Snakemake :")
print("levenshtein")
groups_snk_lev , groups_snk_lev_index = simil_process.grouping_simple(mat_snk_lev,snk_proc)

filename = "../json/source_files/results/group_snk_lev.json"
with open(filename,"w") as f:
    json.dump(groups_snk_lev,f)
    print(filename)
 

filenames = ["../json/source_files/results/group_nf_lev.json",
            "../json/source_files/results/group_snk_lev.json"]

print("total run time "+str(time.time()-time0))

# Step 4 : make the json and dataframe for the groups and group the dataframe with regards to the number of workflows a process is in


print(" MAKING THE DATAFRAMES" )

print("Nextflow :")
print("levenshtein")

nf_lev_json, nf_lev_df = simil_process.sim_to_df(groups_nf_lev,dict_nf,"nf")
df_lev_nf_wf = simil_process.grouping_sim_df_wf(nf_lev_df,len(nf_lev_json))

filename = "../json/source_files/results/sim_nf_lev.json"
filename2 = "../csv/sim_nf_lev_wf.csv"

with open(filename,"w") as f:
    json.dump(nf_lev_json,f)
    print(filename)
df_lev_nf_wf.to_csv(filename2)
    
print("Snakemake :")
print("levenshtein")

snk_lev_json, snk_lev_df = simil_process.sim_to_df(groups_snk_lev,dict_snk,"snk")
df_lev_snk_wf = simil_process.grouping_sim_df_wf(snk_lev_df,len(snk_lev_json))

filename = "../json/source_files/results/sim_snk_lev.json"
filename2 = "../csv/sim_snk_lev_wf.csv"

with open(filename,"w") as f:
    json.dump(snk_lev_json,f)
    print(filename)
df_lev_snk_wf.to_csv(filename2)

print("total run time "+str(time.time()-time0))

#get index for lines containing nfcore processes
idx_nf_core=[]
i=0
for line in nf_lev_json:
    if("nf-core" in line["list_own"]):
        idx_nf_core.append(i)
    i+=1
    
#get only the non nf core proc
nf_lev_non_nfc=[]
i=0
for line in nf_lev_json:
    if(i not in idx_nf_core):
        nf_lev_non_nfc.append(line)
    i+=1

#get only the nf core proc
nf_lev_nfc=[]
i=0
for line in nf_lev_json:
    if(i in idx_nf_core):
        nf_lev_nfc.append(line)
    i+=1
    
nf_lev_nfc = simil_process.remove_nfc_elements(nf_lev_nfc)

print("Non nf-core workflows :")
print("Non nf-core")

nf_lev_df_non_nfc = pd.DataFrame(nf_lev_non_nfc)
df_lev_nf_non_nfc_wf = simil_process.grouping_sim_df_wf(nf_lev_df_non_nfc,len(nf_lev_json))

filename = "../json/source_files/results/sim_nf_lev_non_nfc.json"
filename2 = "../csv/sim_nf_lev_non_nfc_wf.csv"

with open(filename,"w") as f:
    json.dump(nf_lev_non_nfc,f)
    print(filename)
df_lev_nf_non_nfc_wf.to_csv(filename2)


print("nf-core")

nf_lev_df_nfc = pd.DataFrame(nf_lev_nfc)
df_lev_nf_nfc_wf = simil_process.grouping_sim_df_wf(nf_lev_df_nfc,len(nf_lev_json))

filename = "../json/source_files/results/sim_nf_lev_nfc.json"
filename2 = "../csv/sim_nf_lev_nfc_wf.csv"

with open(filename,"w") as f:
    json.dump(nf_lev_nfc,f)
    print(filename)
df_lev_nf_nfc_wf.to_csv(filename2)

























