# `multi`

This pipeline is used in situations when analyzing cell multiplexing data or projects with samples that have both gene expression and VDJ captures. More information about this analysis and when to use it can be found at 10x support webpages:

[Cell Multiplexing with cellranger multi](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/multi)

[Gene Expression, V(D)J & Feature Barcode Analysis with cellranger multi](https://support.10xgenomics.com/single-cell-vdj/software/pipelines/latest/using/multi)

```
./scMaestro multi -h
usage: scMaestro multi [-h] -f [FASTQPATH [FASTQPATH ...]] -g GENOME -r
                       REFERENCE FOLDER [--chain {auto,TR,IG}]
                       [--fullanalysis] -l LIBRARY_CONFIG [--vdj_ref VDJ_REF]
                       [--cmo] [--count]

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
  --chain {auto,TR,IG}  Force the analysis to be carried out for a particular
                        chain type.
  --fullanalysis        Run full analysis pipeline
  -l LIBRARY_CONFIG, --library_config LIBRARY_CONFIG
                        CSV file with the library configration.
  --vdj_ref VDJ_REF     Reference folder for VDJ data
  --cmo                 CMO information will be used for multi analysis
  --count               Run cellranger count for projects with HTO libraries
                        with more 10 individuals mixed.
```


The libraries csv file would also need to be supplied in `config.py`. For example:

```
libraries="libraries.csv"
```

The libraries file would contain the final sample name, flowcell, demultiplex sample name, and library type for each sample. For example:

```
Name,Flowcell,Sample,Type
IL15_LNs,H7CNNBGXG,IL15_LNs,Gene Expression
IL15_LNs,H7CT7BGXG,IL15_LNs_BC,Antibody Capture
IL15_TUMOR_CD11,H7CNNBGXG,IL15_TUMOR_CD11,Gene Expression
IL15_TUMOR_CD11,H7CT7BGXG,IL15_TUMOR_CD11_BC,Antibody Capture
```

* Final sample name will be the name that is given to CellRanger as the name of the sample. 
* Flowcell is the flowcell that contains the FASTQ files for this set of data. This can be the full path or just a unique identifier since the script will pull the full path from the config.py file.
* Sample is the sample name that was used when demultiplexing using `cellranger mkfastq`, and so should match the FASTQ files.
* Type is the library type for each sample. Current supported options are: Gene Expression, VDJ, CRISPR Guide Capture, Antibody Capture, and Multiplexing Capture

The pipeline will use the provided libraries file to make a library file for each individual sample. This will then be processed again to create the configuration file in the format expected by CellRanger. Due to the lack of CRISPR projects at the facility, the pipeline was never tested for this technology. If this pipeline is run on a sample with CRISPR capture, check the generated sample configuration file to ensure that it matches what is expected. 

For multi task with VDJ libraries, “donor” and “origin” are required in "libraries.csv" for aggregation. The link (here) shows how the donor and origin information will be used in the data analysis:

* Donor: An individual from whom adaptive immune cells (T cells, B cells) are collected (e.g. a sister and a brother would each be considered unique donors for the purposes of V(D)J aggregation).
* Origin: The specific source from which a dataset of cells is derived.

```
Name,Flowcell,Sample,Type,Donor,Origin
```

The chain information is specified in `feature_types` column. Valid specifications include `VDJ`, `VDJ-T`, `VDJ-B`, or `VDJ-T-GD`, and the combinations:

* VDJ-T & VDJ-B
* VDJ-T-GD & VDJ-B
* VDJ-T & VDJ-T-GD & VDJ-B

For `multi` task with CRISPR Guide Capture libraries, `feature_reference` column is required to be put in the fifth column in `libraries.csv`. 

```
Name,Flowcell,Sample,Type,Feature
F1Test,AACCCHVM5,F1CRISPR_Library,Gene Expression,crispr_feature_reference1.csv
F1Test,AACCCHVM5,F1GE_Library,CRISPR Guide Capture,crispr_feature_reference1.csv
F2Test,AACCCHVM5,F2CRISPR_Library,Gene Expression,crispr_feature_reference2.csv
F2Test,AACCCHVM5,F2GE_Library,CRISPR Guide Capture,crispr_feature_reference2.csv
F3Test,AACCCHVM5,F3CRISPR_Library,Gene Expression,crispr_feature_reference3.csv
F3Test,AACCCHVM5,F3GE_Library,CRISPR Guide Capture,crispr_feature_reference3.csv
```

The descriptions of the feature reference CSV file can be found [here](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis#feature-ref). In case of varying feature references for different GEX/CRISPR pairs, the fifth column can be used to provide different references.

If an antibody capture was used, then a feature reference file will need to be provided in the `config.py` file with a features entry. There is currently no pipeline flag to add this, and it will need to be provided manually. For example:

```
features="features.csv"
```

The feature reference file would contain (at minimum) a **unique ID**for the feature, human readable name, read, pattern, sequence, and feature type. For example:

```
id,name,sequence,feature_type,read,pattern
CITE_CD64,CD64,AGCAATTAACGGGAG,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_F4_80,F4_80,TTAACTTCAGCCCGT,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_CD8a,CD8a,TACCCGTAATAGCGT,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_XCR1,XCR1,TCCATTACCCACGTT,Antibody Capture,R2,5PNNNNNNNNNN(BC)
```

> No space is allowed for the `id` field and the `id` must be unique.  

Unless the information is provided, it is probably easiest to determine the pattern by checking the FASTQ file for the sequence location. More information can be found at: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis

If a multiplexing capture was used, then the pipeline can be called with the cmo flag. This will add a cmo entry into the config.py file, which can then be edited to provide the cmo (cell multiplexing oligo) reference file. For example:

```
cmo="cmo.csv"
```

The cmo reference file has a very similar format to the feature reference file. The difference is that the feature type would be Multiplexing Capture. For example:

```
id,name,sequence,feature_type,read,pattern
HTO_1,HTO_1,GTCAACTCTTTAGCG,Multiplexing Capture,R2,5P(BC)
HTO_2,HTO_2,TGATGGCCTATTGGG,Multiplexing Capture,R2,5P(BC)
HTO_3,HTO_3,TTCCGCCTCTCTTTG,Multiplexing Capture,R2,5P(BC)
HTO_4,HTO_4,AGTAAGTTCAGCGTA,Multiplexing Capture,R2,5P(BC)
```

When the cmo information is filled into the sample configuration file, it will directly use the cmo ID as the multiplexing sample ID. This would need to be manually edited if a different entry would want to be included.


Once all the supplemental information is filled, use the rerun option in the wrapper to start the pipeline.

If the CellRanger only analysis was requested, then for 15 samples the pipeline will run the following jobs for single cell multi analysis.


> If there are multiple libraries with different features used, you can set `cmo` as a dictionary with the library Name as key and cmo csv file as value:

```
cmo={"CD8_d8_1": "cmo1.csv", "CD8_d8_2": "cmo2.csv", "CD8_d8_3": "cmo3.csv"}
```



There is currently no downstream analysis pipeline, and so if it is requested the CellRanger only pipeline would still be run.

* > Note: The `premrna` flag is deprecated and not used anymore. The exclude-introns can be used to disable include-introns flag in CellRanger. 
* > Note: The `force` flag and expect flag can be used to use the `force-cells` flag and `expect-cells` when running the CellRanger multi analysis. The `force` flag and `expect` flag are mutually exclusive. 


> A Special case (multi with VDJ analysis for selective samples only): 

> * There may be a project where some samples would require GEX, ADT, but not VDJ analysis while other samples from the same project would require all three analyses. For example: GEX1 and GEX2 are T-cell populations and that is the reason they have GEX and ADT only. While, only GEX3 and GEX4 have VDJ.




Cellranger multi does not support HTO libraries with > 12 multiplexing tags. For projects with this case, we can use --count flag to enable the snakemake pipeline to run ‘cellranger count’. 
Please see the link below for an example of the command line and config.py:

https://github.com/CCRSF-IFX/SF-project-tracking/issues/1#issuecomment-1934959534

An example of ‘libraries.csv’ can be obtained in the link below:
https://github.com/CCRSF-IFX/SF-project-tracking/issues/1#issuecomment-1934963263

The type of HTO libraries are set to “Custom”. 

An example of features.csv file can be obtained in the link below:
https://github.com/CCRSF-IFX/SF-project-tracking/issues/1#issuecomment-1934964902

The feature_type of HTO barcodes are set to “Custom”. 
