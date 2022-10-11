#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 00:05:02 2022

@author: marinedjaffardjy
"""

### this script computes levenshtein for nf proc with tools, nf proc without tools, snk proc with tools
### it also computes levenshtein for workflows -- using batches (?)
import json
import jellyfish
import numpy
import pandas as pd
import math
import time

################
# DEFINING VARIABLES
################

################
# IMPORTING THE FILES
################

##import snakemake rules
#with open('/home/marinedjaffardjy/Documents/Code/Similarite_process/json/snk_rules_no_tools.json') as f:
#    snk_rules_no_tools = json.load(f)
##import snakemake rule with tools
#with open('json/snk_rule_info_tool.json') as f:
#    snk_tools = json.load(f)
#with open("/home/marinedjaffardjy/Documents/Code/Similarite_process/json/nf_rules_no_tools.json") as f:
#    nf_rules_no_tools = json.load(f)  

time1 = time.time()
    
with open("/home/marinedjaffardjy/Documents/Code/Similarite_process/json/nf_proc_tool_shell.json") as f:
    nf_rules_tools_shell = json.load(f)
    
with open('../json/snk_proc_tool_shell.json') as f:
    snk_rules_tools_shell= json.load(f)
    
################
# DEFINING THE FUNCTIONS
################    
    
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
    #if(resume>0):
        #with open(outputfile_resume) as f:
            #scores = json.load(f)
            #f.close
    #else :
        #scores = []
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
            if(l==0):
                lev=0
            else:
                lev=(l-score)/l
            scores.append({"rule1":rule1["name"],
                           "rule2":rule2["name"],
                           "levenshtein":lev})
        if(len(v2)>=2):
            v2 = v2[1:]
        
        #save all scores for 50 processes
        if(i%50==0 or i ==len(v1) ):
            with open(output_file+"_"+str(i+resume)+".json","w") as f:
                print(output_file+"_"+str(i+resume)+".json")
                json.dump(scores,f)
                f.close
                scores = []
                print(time.time()-time1)
    return scores

#### launch script
 
snk_proc_path = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_snk_tools_shell/levenshtein_snk_tools_shell"   
nf_proc_path = "/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools_shell/levenshtein_nf_tools_shell"

##nf tools proc shell
#nf_scores_shell = levenshtein_proc_shell(nf_rules_tools_shell,0,nf_proc_path)

#snk tools proc shell
snk_scores_shell = levenshtein_proc_shell(snk_rules_tools_shell,0,snk_proc_path)


#snk_scores = levenshtein_proc(snk_tools,500,snk_proc_path)


#nf tools proc

#nf_scores = levenshtein_proc(nf_rules_tools,3850,nf_proc_path,outputfile_resume="/home/marinedjaffardjy/Documents/Code/Similarite_process/json/levenshtein_nf_tools/levenshtein_nf_tools_3800.json")

#snk_no_tools_scores = levenshtein_proc(snk_rules_no_tools,0,snk_all_path)

#nf_no_tools_scores = levenshtein_proc(nf_rules_no_tools,0,nf_all_path)





























