#


## Configuration for `fastq_screen`


The database configuration for `fastq_screen` can be found in `workflow/config/fastq_screen_slurm.conf`. Bowtie2 indexes for different species were created upfront and the absolute path with prefix of the index are provided. You can modify the file based on your need. 

## Configuration for `kraken2`

Three files below are used as database for `kraken2`: 
```
hash.k2d
opts.k2d
taxo.k2d
```

Please change the path of `kraken2db` in  `workflow/config/program.py`. 


## Configuration for HPC


You need to modify the `singularity-args` and `default-resources` parameters in `workflow/profile/slurm/config.v8+.yaml` according to the required storage space and partition details.

To customize the `workflow/profile/slurm/config.v8+.yaml` file for your specific storage and partition requirements, modify the `singularity-args` and `default-resources` parameters as needed.

1. `singularity-args`: Adjust this to specify the necessary bind paths for your workflow. These paths should point to storage locations on your system. For example:

```
singularity-args: ' "--cleanenv --no-home -B /scratch/ccrsf_scratch -B /mnt/ccrsf-static -B /mnt/ccrsf-ifx -B /mnt/ccrsf-raw -B /mnt/ccrsf-active" '
```

* --cleanenv: Ensures a clean environment within the container.
* --no-home: Disables binding of the home directory.
* -B <path>: Specifies bind paths for directories required by your workflow.

2. `default-resources`: Adjust these parameters to reflect your job's runtime, memory, disk space, and SLURM partition requirements.

```
default-resources:
  runtime: 7200             # Maximum runtime in seconds (2 hours)
  mem_mb: 100000            # Memory allocation in MB (100 GB)
  disk_mb: 1000000          # Disk space allocation in MB (1 TB)
  slurm_partition: "norm"   # Target SLURM partition
```

Be sure to align these settings with the actual storage paths and resource quotas for your computing environment.
