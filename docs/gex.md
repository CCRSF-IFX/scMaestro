# Subcommand `rna`

## Workflow `rna` usage

```
./scMaestro rna -h 
usage: scMaestro rna [-h] -f [FASTQPATH [FASTQPATH ...]] -g GENOME -r
                     REFERENCE FOLDER [--fullanalysis]
                     [--force FORCE | --expect EXPECT] [--exclude-introns]

optional arguments:
  -h, --help            show this help message and exit
  -f [FASTQPATH [FASTQPATH ...]], --fastqs [FASTQPATH [FASTQPATH ...]]
                        Path(s) to fastq files, multiple paths can be provided
                        together. eg. "-f path1 path2"
  -g GENOME, --genome GENOME
                        Genome build, e.g. "hg38", "mm10"
  -r REFERENCE FOLDER, --reference REFERENCE FOLDER
                        Reference folder for alignment. VDJ reference is
                        needed if subcommand "vdj" is used.
  --fullanalysis        Run full analysis pipeline
  --force FORCE         Run Cell Ranger with --force-cell
  --expect EXPECT       Run Cell Ranger with --expect-cells
  --exclude-introns     Exclude intronic reads in count. To maximize
                        sensitivity for whole transcriptome 3’/5’ Single Cell
                        Gene Expression and 3’ Cell Multiplexing experiments,
                        introns will be included in the analysis by default
                        for cellranger (>v7.0.0) count and multi.
```

## Option '--fullanalysis'

If `--fullanalysis` is enabled. Quality control, PCA, clustering, annotation will be performed for each sample seperately using `Seurat` and `SingleR`. An html report will be generated. An example can be found [here](https://github.com/CCRSF-IFX/SF_sc-smk-wl/blob/main/data/10k_PBMC_3p_nextgem_Chromium_X_sc_report.html). 