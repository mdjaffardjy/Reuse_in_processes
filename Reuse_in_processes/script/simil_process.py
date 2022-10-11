#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 18:51:00 2022

@author: marinedjaffardjy

This script contains the functions necessary for computing the semantic similarity scores
for the code of processes in nextflow and snakemake

In order to use this functions you will need :
    - a list of dict for the processes with the keys
    - a list of dict for the workflows 
"""
import json
import jellyfish
import numpy as np
import pandas as pd
import math
import time
import ngram


#compute levenshtein for snakemake
def levenshtein_proc(rules, resume=0, output_file = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein/levenshtein_tool_snk"):
    #input : 
    #    list of snakemake rules in form of a json
    #    resume : int at which the computation will be restarted
    #    output_file : string model of the names for the output files
    #    output_file_resume : string file for the scores already computed in the case of a resume
    #output : table of dict with scores. also saves the scores for all pairs of processes in json (path )
    v1 = rules.copy()[resume:-1]
    v2 = rules.copy()[resume+1:]
    i = 0
    scores = []
    
    #compute score for proc1 and all other processes after it in the list
    for rule1 in v1:
        print(str(i)+"/"+str(len(v1)))
        i+=1
        for rule2 in v2:
            score = jellyfish.levenshtein_distance(rule1['code'],rule2['code'])
            l = max(len(rule1['code']),len(rule2['code']))
            scores.append({"rule1":rule1["wf_orig"]+"/"+rule1["name"],
                           "rule2":rule2["wf_orig"]+"/"+rule2["name"],
                           "levenshtein":(l-score)/l})
        if(len(v2)>=2):
            v2 = v2[1:]
        
        #save all scores for 50 processes
        if(i%50==0 or i ==len(v1) ):
            with open(output_file+"_"+str(i+resume)+".json","w") as f:
                print(output_file+"_"+str(i+resume)+".json")
                json.dump(scores,f)
                f.close
                scores = []
    return scores

def levenshtein_proc_shell(rules, resume=0, output_file = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein/levenshtein_test"):
    #input : 
    #    list of snakemake rules in form of a json
    #    resume : int at which the computation will be restarted
    #    output_file : string model of the names for the output files
    #    output_file_resume : string file for the scores already computed in the case of a resume
    #output : table of dict with scores. also saves the scores for all pairs of processes in json (path )
    v1 = rules.copy()[resume:-1]
    v2 = rules.copy()[resume+1:]
    i = 0
    scores = []
    
    #compute score for proc1 and all other processes after it in the list
    for rule1 in v1:
        print(str(i)+"/"+str(len(v1)))
        i+=1
        for rule2 in v2:
            code1 = rule1['shell_modif']
            code2 = rule2['shell_modif']
            score = jellyfish.levenshtein_distance(code1,code2)
            l = max(len(code1),len(code2))
            scores.append({"rule1":rule1["wf_orig"]+"/"+rule1["name"],
                           "rule2":rule2["wf_orig"]+"/"+rule2["name"],
                           "levenshtein":(l-score)/l})
        if(len(v2)>=2):
            v2 = v2[1:]
        
        #save all scores for 50 processes
        if(i%50==0 or i ==len(v1) ):
            with open(output_file+"_"+str(i+resume)+".json","w") as f:
                print(output_file+"_"+str(i+resume)+".json")
                json.dump(scores,f)
                f.close
                scores = []
    return scores

def ngram_proc(rules, output_file , resume=0,n_size=3):
    #input : 
    #    list of snakemake rules in form of a json
    #    resume : int at which the computation will be restarted
    #    output_file : string model of the names for the output files (ex : "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/ngram_snk_tool")
    #output : table of dict with scores. also saves the scores for all pairs of processes in json (path )
    v1 = rules.copy()[resume:-1]
    v2 = rules.copy()[resume+1:]
    i = 0
    scores = []
    
    time1= time.time()
    for rule1 in v1:
        print(str(i)+"/"+str(len(v1)))
        i+=1
        for rule2 in v2:
            score = ngram.NGram.compare(rule1['code'],rule2['code'],N=n_size)
            scores.append({"rule1":rule1["wf_orig"]+"/"+rule1["name"],
                           "rule2":rule2["wf_orig"]+"/"+rule2["name"],
                           "ngram":score})
        if(len(v2)>=2):
            v2 = v2[1:]
        if(i%50==0 or i ==len(v1) ):
            with open(output_file+"_"+str(i+resume)+".json","w") as f:
                print(output_file+"_"+str(i+resume)+".json")
                json.dump(scores,f)
                f.close
                scores = []
            
            print("time elapsed : "+str(time.time()-time1)+" sec ")
    return scores



def make_score_matrices(nb_proc,path_matrix,path_scores,model_filename,score_name):
    #get execution time :
    time1= time.time()
    #list the scores filenames and sizes
    sizes=[]
    filenames=[]
    path_model=path_scores+"/"+model_filename
    i=50
    while i <=(nb_proc-1):
        filenames.append(path_model+str(i)+".json")
        i+=50
        sizes.append(50)
    if((nb_proc-1)%50!=0):
        filenames.append(path_model+str(nb_proc-1)+".json")
        sizes.append((nb_proc-1)%50)
    
    
    #open each file and make a matrix out of it in another file : each matrix file contains 50 lines
    z=0
    x=0
    j=nb_proc-1
    matrix_filenames=[]
    for k in range (0,len(filenames)):
        file=filenames[k]
        new_matrix=[]
        x+=sizes[k]
        with open(file) as f:
            new_lines=json.load(f)
        for i in range(0,sizes[k]):
            new_scores=[el[score_name] for el in new_lines[0:j-z]]
            scores_el = [1]+new_scores
            zeros = np.zeros(z)
            z+=1
            new_matrix.append(list(zeros)+scores_el)
            new_lines=new_lines[j-z:]   
        matrix_filename= path_matrix+"/matrix_"+str(x)+".json"
        matrix_filenames.append(matrix_filename)
        #print(np.shape(new_matrix)) 
        print(matrix_filename)
        with open(matrix_filename,"w") as file_json:
            json.dump(new_matrix,file_json)
        print(time.time()-time1)
    return matrix_filenames

def get_matrix_files(path_matrix,nb_proc):
    mat_nf_ngram=[]
    i=50
    while i <=(nb_proc-1):
        matrix_filename= path_matrix+"/matrix_"+str(i)+".json"
        mat_nf_ngram.append(matrix_filename)
        i+=50
    if((nb_proc-1)%50!=0):
        matrix_filename= path_matrix+"/matrix_"+str(nb_proc-1)+".json"
        mat_nf_ngram.append(matrix_filename) 
    return mat_nf_ngram

def grouping_simple(matrix_list,obj_list,treshold=0.85,ignore_nf=[]):
    #this function helps making groups by using a similarity matric split in different files
    #input:
    #matrix_list = a list of files where the matrices are
    #obj_list = a list of the proc dict in order to have a list of dict of the processes for each rule
    #treshold = treshold for making the groups
    #ignore_nf = indexes of additional proc to ignore (we want to ignore the ones in nf core sometimes)
    #output = list of dict and list of indexes of rules
    
     #get execution time :
    time1= time.time()
    to_ignore=ignore_nf #add proc in wf nfcore indexes
    groups=[]
    line_nb=0
    for file_matrix in matrix_list:
        print(file_matrix)
        with open(file_matrix) as f:
            matrice=json.load(f)
        for line in matrice:
            if line_nb not in to_ignore:
                new_group=[line_nb]
                for j in range(0,len(line)):
                    if(matrice[line_nb%50][j]>treshold):
                        new_group.append(j)
                groups.append(list(set(new_group)))
                to_ignore+=new_group
            line_nb+=1
            
    #turn the groups into lists of snk or nf rules
    simil_obj=[]
    for group in groups:
        group_obj = []
        for el in group:
            group_obj.append(obj_list[el])
        simil_obj.append(group_obj)
    print(len(simil_obj))
    print(time.time()-time1)
    return simil_obj, groups


def sim_to_df(groups_list, dict_wf,sys):
    #takes the groups list of list of dict and outputs a list of dict with info about the groups
    #output : list of dict, equivalent dataframe
    groups_sim_df = []
    for group in groups_list :
        list_own = []
        list_wf = []
        list_wf_names = []
        list_contrib = []
        tools=[]
        list_proc=[]
        for el in group :
            list_own.append(el['owner'])
            list_wf.append(el['wf_orig'])
            tools+=el["tools"]
            if sys=='nf':
                name_wf = el['owner']+'/'+el['wf_orig']
            if sys=='snk':
                name_wf = el['wf_orig']
            list_wf_names.append(name_wf)
            list_proc.append(name_wf+"/"+el['name'])    
            if (name_wf in dict_wf.keys()):
                for contr in dict_wf[name_wf]['contributors']:
                    list_contrib.append(contr)
            elif (name_wf+".nf" in dict_wf.keys()):
                for contr in dict_wf[name_wf+".nf"]['contributors']:
                    list_contrib.append(contr)
        list_own = list(set(list_own))
        list_wf = list(set(list_wf))
        list_contrib = list(set(list_contrib))
        #print(group[0]['tools'])
        groups_sim_df.append({'nb_reuse' : len(group),
                              'tools' : list(set(tools)),
                              'nb_own' : len(set(list_own)),
                              'list_own' : list_own ,
                              'nb_wf' : len(set(list_wf)),
                              'list_wf' : list(set(list_wf)),
                              'list_contrib' : list(set(list_contrib)),
                              'nb_contrib' :len(set(list_contrib)),
                              'codes':[el["code"] for el in group],
                             'list_proc':list_proc,
                             'list_wf_names':list(set(list_wf_names))})
    #print(groups_sim_df)
    return groups_sim_df,pd.DataFrame(groups_sim_df)

# group the processes per nb of times reused
def grouping_sim_df (df_sim_n,nb_groups,dict_wf ):
    df_sim = df_sim_n.copy()
    tot_group = nb_groups
    vals = set(list(df_sim["nb_reuse"])+list(df_sim["nb_wf"])+list(df_sim["nb_own"]))
    tot_wf = len(dict_wf)
    tot_own = np.sum(df_sim_n["nb_own"])

    df_sim_group = pd.DataFrame(columns=["nb_reuse", "nb_proc","prop_proc","nb_own","prop_own","nb_wf","prop_wf"])
    for val in vals :
        nb_proc = len(df_sim.loc[df_sim["nb_reuse"]==val])
        prop_proc = nb_proc/tot_group
        nb_own = len(df_sim.loc[df_sim["nb_own"]==val])
        prop_own = nb_own/tot_group
        nb_wf = len(df_sim.loc[df_sim["nb_wf"]==val])
        prop_wf = nb_wf/tot_group
        df_sim_group = df_sim_group.append({"nb_reuse":val,
                                            "nb_proc":nb_proc,
                                            "prop_proc":prop_proc*100.0,
                                            "nb_own":nb_own,
                                            "prop_own":prop_own*100.0,
                                            "nb_wf":nb_wf,
                                            "prop_wf":prop_wf*100.0}, ignore_index = True)
    
    return df_sim_group.sort_values(by=["nb_reuse"], ascending=True)




def grouping_sim_df_wf (df_sim_n,nb_groups,dict_wf,dict_auth):
    df_sim = df_sim_n.copy()
    vals = set(df_sim["nb_wf"])
    tot_group = nb_groups

    df_sim_group = pd.DataFrame(columns=["nb_proc","prop_proc","nb_wf"])
    for val in vals :
        sec_df = df_sim.loc[df_sim["nb_wf"]==val]
        nb_proc = len(sec_df)
        prop_proc = nb_proc/tot_group
        df_sim_group = df_sim_group.append({"nb_proc":nb_proc,
                                            "prop_proc":prop_proc*100.0,
                                            "nb_wf":val}, ignore_index = True)
    
    return df_sim_group.sort_values(by=["nb_wf"], ascending=False)



















