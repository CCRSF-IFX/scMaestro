# scMaestro

`scMaestro`, developed by CCRSF IFX, is aim to provide an end-to-end solution for single cell sequencing data. 

## Quick start

To run `scMastro`, activation of an conda environment `singularity` are required.

* Clone git repo

```
git clone --recurse-submodules https://github.com/CCRSF-IFX/scMaestro.git
cd scMaestro/
```

* Install conda environment: 

```
conda env create -n scMastro -f environment.yml
```

You only need to run the command above once. 

* Activate conda environment 


```
conda activate scMastro
```

* Run `scMastro`

```
./scMastro 

usage: scMaestro [-h]
                 {rna,multi,vdj,atac,multiome,fixedrna,rerun,dryrun,unlock}
                 ...

scMastro: Comprehensive workflow for processing single cell sequencing data

positional arguments:
  {rna,multi,vdj,atac,multiome,fixedrna,rerun,dryrun,unlock}
                        sub-command help
    rna                 Snakemake pipeline for 10x scRNA-seq data analysis
    multi               Snakemake pipeline for 10x CellRanger multi data
                        analysis
    vdj                 Snakemake pipeline for 10x VDJ data
    atac                Snakemake pipeline for 10x scATAC-seq data analysis
    multiome            Snakemake pipeline for 10x Multiome ATAC + GEX data
    fixedrna            Snakemake pipeline for 10x Fixed RNA profiling (FRP)
                        data
    rerun               Equavalent of snakemake --rerun
    dryrun              Equavalent of snakemake --dryrun
    unlock              Equavalent of snakemake --unlock

optional arguments:
  -h, --help            show this help message and exit
```



