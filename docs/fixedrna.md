## Single Cell Fixed RNA Profiling workflow: `fixedrna`

### Information required before running the pipeline

* Reference/Probe_set 

* Singleplex or multiplex library 



### How to run 

```
./scMaestro fixedrna --help 
usage: scMaestro fixedrna [-h] -f [FASTQPATH [FASTQPATH ...]] -g GENOME -l
                          LIBRARY_CONFIG --probe_set PROBE_SET [--singleplex]
                          [--multiplex MULTIPLEX]

optional arguments:
  -h, --help            show this help message and exit
  -f [FASTQPATH [FASTQPATH ...]], --fastqs [FASTQPATH [FASTQPATH ...]]
                        Path(s) to fastq files, multiple paths can be provided
                        together. eg. "-f path1 path2"
  -g GENOME, --genome GENOME
                        Genome build, e.g. "hg38", "mm10"
  -l LIBRARY_CONFIG, --library_config LIBRARY_CONFIG
                        CSV file with the library configration.
  --probe_set PROBE_SET
                        Probe set for FRP data
  --singleplex          Singleplex FRP
  --multiplex MULTIPLEX
                        Mutiplexing information for FRP
```

The parameters `--singleplex` and `--multiplex` are mutually excluesive and at least one of them has to be specified.

Here is an exmaple of `config.py` file: 

```
unaligned=["/mnt/ccrsf-static/Analysis/xies4/github_repos/pipeline_dev_test/raw_fastq/fixedrna/221102_VH00271_218_AAC3K5WM5/AAC3K5WM5/outs/fastq_path/AAC3K5WM5"]
analysis="/mnt/ccrsf-static/Analysis/xies4/github_repos/pipeline_dev_test/test_fixedscRNA_singleplex/BaoTran_CS033083_1scRNAseq_FixedRNA_101422/Analysis"
ref="hg38"
projectname="BaoTran_CS033083_1scRNAseq_FixedRNA_101422"
libraries="libraries.csv"
probe_set="/mnt/ccrsf-ifx/Software/tools/GemCode/cellranger-7.0.1/probe_sets/Chromium_Human_Transcriptome_Probe_Set_v1.0_GRCh38-2020-A.csv"
pipeline="fixedrna"
aggregate=False # Default value for fixedrna
```

Here is `libraries.csv`:

Name,Flowcell,Sample,Type
LIB1,AAC3K5WM5,LIB1,Gene Expression
LIB2,AAC3K5WM5,LIB2,Gene Expression
LIB3,AAC3K5WM5,LIB3,Gene Expression

For multiplexed libraries, here is the config file: 


```
unaligned=["/mnt/ccrsf-static/Analysis/xies4/github_repos/pipeline_dev_test/test_fixedscRNA/223LH3LT1/outs/fastq_path/223LH3LT1"]
analysis="/mnt/ccrsf-static/Analysis/xies4/github_repos/pipeline_dev_test/test_fixedscRNA/Analysis"
ref="hg38"
projectname="DanielMcVicar_CS036898_4fixedscRNA_07302024"
pipeline="fixedrna"
probe_set="/mnt/ccrsf-ifx/Software/tools/GemCode/cellranger-8.0.1/probe_sets/Chromium_Human_Transcriptome_Probe_Set_v1.0.1_GRCh38-2020-A.csv"
libraries="libraries.csv"
multiplex="multiplex.csv"
aggregate=False # Default value for fixedrna 
```


`libraries.csv` is the sample as singleplex library. 

Here is an example for `multiplex.csv`
```
Name,sample_id,probe_barcode_ids,description
pool_1,Young_RepSox_3nM,BC001,Young_RepSox_3nM
pool_1,Young_PC3EVNeut,BC002,Young_PC3EVNeut
pool_2,Young_Enza_20uM,BC001,Young_Enza_20uM
pool_2,Aged_PC3EV,BC002,Aged_PC3EV
pool_3,Young_Combo,BC001,Young_Combo
pool_3,MDA_PCa2b,BC004,MDA_PCa2b
pool_4,Young_PC3EV,BC001,Young_PC3EV
pool_4,Young_PC3Stat5,BC002,Young_PC3Stat5
```

