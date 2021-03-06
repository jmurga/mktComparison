# Comparison of four hierachical McDonald and Kreitman test approaches using real and simulated population data

Here, we perform a comparison of four hierarchical MKT methods: (i) the standard (original) MKT (sMKT, McDonald and Kreitman 1991); (ii) the Fay, Wickoff and Wu correction (FWWMKT, Fay 2001); (iii) a new imputation method based on FWWMKT (imputationMKT)the Extended MKT (eMKT, Mackay et al. 2012); and (iv) the asymptotic MKT (aMKT, Messer and Petrov 2012). 

Both real and simulated population genomics data are used to assess their performance for different evolutionary scenarios. Genome-wide DNA variation data come from two *Drosophila melanogaster* and two human populations (one colonizing and one ancestral population, in each case). Simulated data was generated with the SLiM 3 evolutionary framework (Haller ‎2019). We test several conditions including gene-to-gene vs gene concatenating analysis, or the effect of recombination on the power and bias of selection estimates of the different MKT methods.


This repository only include raw code to get main results. notebooks/ folder include Jupyter Notebooks running on Python 3.6 kernel to execute step by step the pipeline. src/ folder contain raw scripts to needed to execute the pipelin. Please note that multiple step could be parallelized, in this case create yourself customs bash scripts or run it on your server manually.  

Pipeline were developed with the following [conda enviroment](https://github.com/jmurga/mktComparison/blob/master/mktComparison.yml) in local server: 100GB RAM and 16 Intel(R) Xeon(R) CPU.  

Pipelines execution requiere to download  files. Paths would need to be changed too.

## Data retrieve
Pipelines execution requiere to download the following files. Paths would need to be changed too. 

### *D. melanogaster* population genomic data.
Variation data generated by the Drosophila Genome Nexus, together with divergence data between D. melanogaster and D. simulans, was retrieved from PopFly ([Hervás et al. 2017](https://academic.oup.com/bioinformatics/article/33/17/2779/3796397)) in FASTA format (also available in [DGN web site](http://www.johnpool.net/genomes.html)). Recomb data from [Comeron et al. 2012](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1002905)  

#### [01_*D. melanogaster* pipeline (python/bash)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/dmelProteinsData.ipynb)  

### Human population genomic data. 
Genome variation data and information of the ancestral state of the variants generated by the 1000GP Phase III (1000 Genomes Project Consortium 2015), together with divergence between humans and chimpanzees, were retrieved from PopHuman ([Casillas et al. 2018](https://academic.oup.com/nar/article/46/D1/D1003/4559406)) in Variant Call Format (VCF). Recomb data from [Bhèrer et al. 2017](https://www.nature.com/articles/ncomms14994). [Pilot mask](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/accessible_genome_masks) to exclude low quality variants download from 1000GP ftp.

#### [02_Human pipeline (python/bash)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/humanProteins.ipynb)

### Simulations
SLiM simulations automatized with *src/scripts/slimProcess.py*. Simulations based on recipes deposited at *scr/slimRecipes*. Please check scripts parameters before execute.

#### [03_Simulations (python)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/SLiMSimulations.ipynb)

## Analysis
#### [04_Alpha and b analysis from simulations (R)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/SLiMAnalysis.ipynb)
#### [05_Gene-by-gene analysis (R)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/alphaTable.ipynb)
#### [06_Concatenation and recombination effect (R)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/concatenation.ipynb)
#### [07_Power (R)](https://github.com/jmurga/mktComparison/blob/master/scripts/notebooks/power.ipynb)
