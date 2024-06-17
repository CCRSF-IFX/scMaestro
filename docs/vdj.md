# `vdj` pipeline

```
usage: scMaestro vdj [-h] -f [FASTQPATH ...] -r REFERENCE FOLDER -g GENOME [-n] [--rerun] [--unlock]
                     [--chain {auto,TR,IG}]

options:
  -h, --help            show this help message and exit
  -f [FASTQPATH ...], --fastqs [FASTQPATH ...]
                        Path(s) to fastq files, multiple paths can be provided together. eg. "-f path1
                        path2"
  -r REFERENCE FOLDER, --reference REFERENCE FOLDER
                        Reference genome folder for alignment
  -g GENOME, --genome GENOME
                        Genome build, e.g. "hg38", "mm10"
  -n, --dryrun          dry run
  --rerun               dry run then prompt for submitting jobs that need to be rerun
  --unlock              unlock working directory
  --chain {auto,TR,IG}  Force the analysis to be carried out for a particular chain type.
```



By default, Cell Ranger will try to automatically determine the chain type from the data. When this fails, the complete error message will look something like the following. In order for Cell Ranger to automatically determine chain type, the sample library must meet the listed conditions.

```
V(D)J Chain detection failed for Sample foo in "/mnt/scratch/inputs/x/y".

Total Reads          = 1000000
Reads mapped to TR   = 49211
Reads mapped to IG   = 3

In order to distinguish between the TR and the IG chain the following conditions need to be satisfied:
- A minimum of 10000 total reads
- A minimum of 5.0% of the total reads needs to map to TR or IG
- The number of reads mapped to TR should be at least 3.0x compared to the number of reads mapped to IG or vice versa
Please check the input data and/or specify the chain via the --chain argument.
```

To overcome this error on the command line, for cellranger vdj explicitly set the --chain parameter to either IG for BCRs or TR for TCRs. Documentation is at https://support.10xgenomics.com/single-cell-vdj/software/pipelines/latest/using/vdj#opt-arg-exp. 


## Reference

https://kb.10xgenomics.com/hc/en-us/articles/10840673911693-How-to-solve-V-D-J-Chain-detection-failed-error-on-10x-Cloud
