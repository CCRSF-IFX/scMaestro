# Demultiplexing and Analyzing 5’ Immune Profiling Libraries Pooled with Hashtags

## Step1: demultiplexing 

### Prepare `config.py` file
```
unaligned=["/scratch/ccrsf_scratch/scratch/Illumina_Demultiplex/NovaSeq/20240816_LH00584_0065_B22NK2FLT3/22NK2FLT3/outs/fastq_path/22NK2FLT3"]
analysis="/mnt/ccrsf-static/singlecell_projects/PamelaSchwartzberg_CS037516_9sclibs_08072024/Analysis_demultiplex"
ref="mm10"
projectname="PamelaSchwartzberg_CS037516_9sclibs_08072024"
yields="1411633.0"
archive=True
runs="20240816_LH00584_0065_B22NK2FLT3"
libraries="libraries.csv"
pipeline="multi"
cmo="cmo.csv"
aggregate=False
```

### Prepare `libraries.csv`

In `libraries.csv`, only `Gene Expression` and `Multiple Capture` samples are included to run `multi` pipeline. The purpose of this step is demultiplexing. 

```
Name,Flowcell,Sample,Type
CD8_d8_1,22NK2FLT3,1_cDNA_CD8_d8_1,Gene Expression
CD8_d8_2,22NK2FLT3,2_cDNA_CD8_d8_2,Gene Expression
CD8_d8_3,22NK2FLT3,3_cDNA_CD8_d8_3,Gene Expression
CD8_d8_1,22NK2FLT3,4_HTO_CD8_d8_1,Multiplexing Capture
CD8_d8_2,22NK2FLT3,5_HTO_CD8_d8_2,Multiplexing Capture
CD8_d8_3,22NK2FLT3,6_HTO_CD8_d8_3,Multiplexing Capture
```

### Prepare `cmo.csv`

```
id,name,sequence,feature_type,read,pattern
A0301,A0301,ACCCACCAGTAAGAC,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0302,A0302,GGTCGAGAGCATTCA,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0303,A0303,CTTGCCGCATGTCAT,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0304,A0304,AAAGCATTCTTCACG,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0305,A0305,CTTTGTCTTTGTGAG,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0306,A0306,TATGCTGCCACGGTA,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0307,A0307,GAGTCTGCCAGTATC,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0308,A0308,TATAGAACGCCAGGC,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0309,A0309,TGCCTATGAAACAAG,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
A0310,A0310,CCGATTGTAACAGAC,Multiplexing Capture,R2,5PNNNNNNNNNN(BC)
``` 

## Step 2: Convert per sample bam files to FASTQs for the GEX data

In this step, you will run the snakemake pipeline to:
1. Convert per-sample BAM file to FASTQ files
2. Prepare the folder for next step

```
conda activate /mnt/ccrsf-ifx/Software/tools/conda_env4scwf
module load samtools
snakemake -s multi_5p_bam2fastq.py --configfile config.yaml --profile ./slurm/  -e cluster-generic -j 20 
```

```
indir: "/mnt/ccrsf-static/singlecell_projects/PamelaSchwartzberg_CS037516_9sclibs_08072024/Analysis_demultiplex/"
outdir: "outdir"
```

```
Job stats:
job                   count
------------------  -------
all                       1
bamtofastq               30
prep_raw_fq_folder       30
total                    61
```


## Step3: Final: Run cellranger multi for GEX, FB, TCR, and BCR data

Only GEX and VDJ data is used in the example project. 

* Prepare fastq files so that the folder structure meets what `cellranger mkfastq` outputs. 


* Prepare `libraries.csv`

In the example we used, there are 3 GEX libraries and each GEX library has 10 samples multiplexed together. So in total, there are 30 samples. There are 3 corresponding VDJ libraries. Since we don't perform demultiplexing using HOT on VDJ data. So for the 10 samples from a particular GEX library, same VDJ data were provided. 

In the `libraries.csv` file below, only samples from `D8_d8_1` are shown. 

```
Name,Flowcell,Sample,Type,force-cells
CD8_d8_1_A0301,22NK2FLT3,CD8_d8_1_A0301,Gene Expression,1049
CD8_d8_1_A0302,22NK2FLT3,CD8_d8_1_A0302,Gene Expression,857
CD8_d8_1_A0303,22NK2FLT3,CD8_d8_1_A0303,Gene Expression,1042
CD8_d8_1_A0304,22NK2FLT3,CD8_d8_1_A0304,Gene Expression,957
CD8_d8_1_A0305,22NK2FLT3,CD8_d8_1_A0305,Gene Expression,986
CD8_d8_1_A0306,22NK2FLT3,CD8_d8_1_A0306,Gene Expression,824
CD8_d8_1_A0307,22NK2FLT3,CD8_d8_1_A0307,Gene Expression,1062
CD8_d8_1_A0308,22NK2FLT3,CD8_d8_1_A0308,Gene Expression,897
CD8_d8_1_A0309,22NK2FLT3,CD8_d8_1_A0309,Gene Expression,825
CD8_d8_1_A0310,22NK2FLT3,CD8_d8_1_A0310,Gene Expression,1179
CD8_d8_1_A0301,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,1049
CD8_d8_1_A0302,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,857
CD8_d8_1_A0303,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,1042
CD8_d8_1_A0304,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,957
CD8_d8_1_A0305,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,986
CD8_d8_1_A0306,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,824
CD8_d8_1_A0307,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,1062
CD8_d8_1_A0308,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,897
CD8_d8_1_A0309,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,825
CD8_d8_1_A0310,22NK2FLT3,7_VDJ_CD8_d8_1,VDJ-T,1179
```

## Reference 

[Demultiplexing and Analyzing 5’ Immune Profiling Libraries Pooled with Hashtags](https://www.10xgenomics.com/analysis-guides/demultiplexing-and-analyzing-5%E2%80%99-immune-profiling-libraries-pooled-with-hashtags)


