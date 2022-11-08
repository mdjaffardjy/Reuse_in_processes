[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Version 1.0.1](https://img.shields.io/badge/version-v1.0.1-blue)]()


# Reuse_in_processes

This repository contains the code for investigating reuse using levenshtein distance in Nextflow and Snakemake processors. 


- In the folder __script__ there is the ["library"](script/simil_process.py) of all methods for computing the similarity scores, grouping the processors and compiling the results in dataframes. The [pipeline](script/run_levenshtein_all.py) contains the pipeline for producing these scores and dataframes.
- In the folder __notebook__ are the [notebooks](/notebook/) in which we visualize our investigation's analyses.

## Source data

The original data that the analysis is performed on can be found in the folder __json/source_files__. In this folder there is [workflow](/json/source_files/wf_new_crawl_nextflow.json) and [author](/json/source_files/author_clem_nf.json) metadata froma crawl of snakemake and nextflow workflows . 
There is also [processors](/json/source_files/nf_proc_tool_shell.json) information files. Note that these are results of the [Nextflow parser] and [Snakemake parser] that were reunited in a single list of dictionnaries in a json, and with an additional "shell" key containing the isolated shell scripts of the processes. They were also filtered to only keep the processors containing at least one tool in a shell.


## Contribute
Please submit GitHub issues to provide feedback or ask for new features, and contact me for any related question.


## To Run

A conda environment can be found here.

### Step 1 : compute the scores and generate dataframes

This step can take a few hours. 

```
python3 script/run_levenshtein_all.py
```

### Step 2 : read notebooks

The [notebooks](/notebook/) containing the analyses can now be launched :
- To take a look at process reuse repartition in workflows in [this notebook](/notebook/Figures_reuse_processes_simil_shell.ipynb). This notebook contains the figures for nextflow and snakemake processors reuse, as well as the comparison between nf-core and non nf-core processors reuse.
- To see the tools repartitions in workflows, the code can be foudn in [this notebook](/notebook/group_patterns_proc.ipynb) 



## License
FAIR-Checker is released under the [MIT License](LICENSE). Some third-party components are included. They are subject to their own licenses. All of the license information can be found in the included [LICENSE](LICENSE) file.


