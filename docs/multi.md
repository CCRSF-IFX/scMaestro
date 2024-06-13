# `multi` pipeline 


This pipeline is used in situations when analyzing cell multiplexing data or projects with samples that have both gene expression and VDJ captures. More information about this analysis and when to use it can be found at:
https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/multi
https://support.10xgenomics.com/single-cell-vdj/software/pipelines/latest/using/multi


The pipeline would be called using subcommand `multi`: 



The libraries csv file would also need to be supplied.

| Name            | Flowcell  | Sample             | Type             |            |
|-----------------|-----------|--------------------|------------------|------------|
| IL15_LNs        | H7CNNBGXG | IL15_LNs           | Gene Expression  | Expression |
| IL15_LNs        | H7CT7BGXG | IL15_LNs_BC        | Antibody Capture | Capture    |
| IL15_TUMOR_CD11 | H7CNNBGXG | IL15_TUMOR_CD11    | Gene Expression  | Expression |
| IL15_TUMOR_CD11 | H7CT7BGXG | IL15_TUMOR_CD11_BC | Antibody Capture | Capture    |

* Final sample name will be the name that is given to CellRanger as the name of the sample. 
* Flowcell is the flowcell that contains the FASTQ files for this set of data. This can be the full path or just a unique identifier since the script will pull the full path from the config.py file.
* Sample is the sample name that was used when demultiplexing, and so should match the FASTQ files.
* Type is the library type for each sample. Current supported options are: Gene Expression, VDJ, CRISPR Guide Capture, Antibody Capture, and Multiplexing Capture

The pipeline will use the provided libraries file to make a library file for each individual sample. This will then be processed again to create the configuration file in the format expected by CellRanger. Due to the lack of CRISPR projects at the facility, the pipeline was never tested for this technology. If this pipeline is run on a sample with CRISPR capture, check the generated sample configuration file to ensure that it matches what is expected. 

For `multi` task with VDJ libraries, “donor” and “origin” are required in "libraries.csv" for aggregation. The link [here](https://support.10xgenomics.com/single-cell-vdj/software/pipelines/latest/using/aggr#donor_origin) shows how the donor and origin information will be used in the data analysis:

* Donor: An individual from whom adaptive immune cells (T cells, B cells) are collected (e.g. a sister and a brother would each be considered unique donors for the purposes of V(D)J aggregation).

* Origin: The specific source from which a dataset of cells is derived.


The chain information is specified in 'feature_types' column. Valid specifications include VDJ, VDJ-T, VDJ-B, or VDJ-T-GD, and the combinations:

• VDJ-T & VDJ-B
• VDJ-T-GD & VDJ-B
• VDJ-T & VDJ-T-GD & VDJ-B


For multi task with CRISPR Guide Capture libraries, "feature_reference" column is required to be put in the fifth column in "libraries.csv". 
Name,Flowcell,Sample,Type,Feature
F1Test,AACCCHVM5,F1CRISPR_Library,Gene Expression,crispr_feature_reference1.csv
F1Test,AACCCHVM5,F1GE_Library,CRISPR Guide Capture,crispr_feature_reference1.csv
F2Test,AACCCHVM5,F2CRISPR_Library,Gene Expression,crispr_feature_reference2.csv
F2Test,AACCCHVM5,F2GE_Library,CRISPR Guide Capture,crispr_feature_reference2.csv
F3Test,AACCCHVM5,F3CRISPR_Library,Gene Expression,crispr_feature_reference3.csv
F3Test,AACCCHVM5,F3GE_Library,CRISPR Guide Capture,crispr_feature_reference3.csv
The descriptions of the feature reference CSV file can be found here. In case of varying feature references for different GEX/CRISPR pairs, the fifth column can be used to provide different references.

If an antibody capture was used, then a feature reference file will need to be provided in the config.py file with a features entry. There is currently no pipeline flag to add this, and it will need to be provided manually. For example:

features="features.csv"

The feature reference file would contain (at minimum) a unique ID for the feature, human readable name, read, pattern, sequence, and feature type. For example:

id,name,sequence,feature_type,read,pattern
CITE_CD64,CD64,AGCAATTAACGGGAG,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_F4_80,F4_80,TTAACTTCAGCCCGT,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_CD8a,CD8a,TACCCGTAATAGCGT,Antibody Capture,R2,5PNNNNNNNNNN(BC)
CITE_XCR1,XCR1,TCCATTACCCACGTT,Antibody Capture,R2,5PNNNNNNNNNN(BC)

Unless the information is provided, it is probably easiest to determine the pattern by checking the FASTQ file for the sequence location. More information can be found at: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/feature-bc-analysis

If a multiplexing capture was used, then the pipeline can be called with the cmo flag. This will add a cmo entry into the config.py file, which can then be edited to provide the cmo (cell multiplexing oligo) reference file. For example:

cmo="cmo.csv"

The cmo reference file has a very similar format to the feature reference file. The difference is that the feature type would be Multiplexing Capture. For example:

id,name,sequence,feature_type,read,pattern
HTO_1,HTO_1,GTCAACTCTTTAGCG,Multiplexing Capture,R2,5P(BC)
HTO_2,HTO_2,TGATGGCCTATTGGG,Multiplexing Capture,R2,5P(BC)
HTO_3,HTO_3,TTCCGCCTCTCTTTG,Multiplexing Capture,R2,5P(BC)
HTO_4,HTO_4,AGTAAGTTCAGCGTA,Multiplexing Capture,R2,5P(BC)

When the cmo information is filled into the sample configuration file, it will directly use the cmo ID as the multiplexing sample ID. This would need to be manually edited if a different entry would want to be included.



