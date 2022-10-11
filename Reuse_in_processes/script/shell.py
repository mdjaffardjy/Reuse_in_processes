#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 15:22:29 2022

@author: marinedjaffardjy
"""
import json
import jellyfish
import numpy as np
import pandas as pd
import math
import re
import time
import os.path
import ntpath

#snakemake rules
with open('/home/marinedjaffardjy/Documents/Code/Investigating_reuse/json/snk_rule_info_tool.json') as f:
    snk_proc = json.load(f)

def parse_lines(compil):
    # returns a list of lines from the shell data
    # input : shell content (string)
    # output : list of command lines as a list of strings
    lines_list = []
    for whole_line in compil.split('\n'):
        # check if the line has at least one character
        if (re.search('[a-zA-Z]', whole_line) is not None):  # checks that the line contains a character
            # split the line into several lines if there is a |, a ; or a >
            if any(ext in whole_line for ext in ['', '|', ';', '>']):
                whole_line = whole_line.split('|')
                for subline in whole_line:
                    subline = subline.split('>')
                    for subsubline in subline:
                        subsubline = subsubline.split(';')
                        for el in subsubline:
                            lines_list.append(el)
    #
    return lines_list

def remove_path_tool(line):
    line2 =line
    while(len(line2)>1 and line2[0]==' '):
        line2 = line2[1:]
    
    line2 = line2.replace('cmd ( "',"")
    tool = line2.split(' ')[0].replace('\t', '').replace('"', '').replace("'", '')  # just for syntax, take out the tabs
    if ('/' in tool):
        tool = path_leaf(tool)
        line_rest=line2.replace(line2.split(' ')[0],"")
        result_line = tool+line_rest
    else :
        result_line = line
    # if the tool is in a command with a path ex /home/marine\.outil
    
    
    return result_line


def path_leaf(path):
    # extract last word from path
    # input : string path name
    # output string last element of path
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def extract_shell_cmd(proc):
    code = proc["code"]
    #extract shell parts
    if( '@workflow.shellcmd') in code:
        code = code.split("@workflow.shellcmd (")[1]
        code = code.split("@workflow.run")[0]
        #print(code)
    #extract comments
    code = re.sub(r'#.*\n?', '', code)
    #remove wildcards
    code = re.sub("\{.*?\}","",code) #remove wildcard input files
    #print(code)
    #remove path from toolnames
    lines = parse_lines(code)
    code_final="\n"
    for line in lines:
        line2=remove_path_tool(line)
        code_final+=line2+"\n"
    #code_final = code_final.replace("\n","").replace("\t","").replace(" ","")
    return code_final


# replace code in proc by code 
i=0
for proc in snk_proc :
    #print(i)
    shell = extract_shell_cmd(proc)
    proc["shell"] = shell
    proc["shell_modif"] = shell.replace("\n","").replace("\t","").replace(" ","")
    i+=1
    
with open('../json/snk_proc_tool_shell.json',"w") as f:
    json.dump(snk_proc,f)
































