#

## Resource allocation 


### Configuration for `fastq_screen`


The database configuration for `fastq_screen` can be found in `workflow/config/fastq_screen_slurm.conf`. Bowtie2 indexes for different species were created upfront and the absolute path with prefix of the index are provided. You can modify the file based on your need. 

### Configuration for `kraken2`

Three files below are used as database for `kraken2`: 
```
hash.k2d
opts.k2d
taxo.k2d
```

Please change the path of `kraken2db` in  `workflow/config/program.py`. 


### Configuration for HPC


You need to modify the `singularity-args` and `default-resources` parameters in `workflow/profile/slurm/config.v8+.yaml` according to the required storage space and partition details.

```
singularity-args: ' "--cleanenv --no-home -B /scratch/ccrsf_scratch -B /mnt/ccrsf-static -B /mnt/ccrsf-ifx -B /mnt/ccrsf-raw -B /mnt/ccrsf-active" '
......
default-resources:
  runtime: 7200
  mem_mb: 100000
  disk_mb: 1000000
  slurm_partition: "norm"
```

