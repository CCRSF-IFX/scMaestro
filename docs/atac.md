# workflow: 'atac'

Workflow 'atac' can analyze 10x scATAC-seq data. 

## Usage 

```
./scMaestro atac -h 
usage: scMaestro atac [-h] -f [FASTQPATH [FASTQPATH ...]] -g GENOME -r
                      REFERENCE FOLDER

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
```


