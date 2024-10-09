conda activate /mnt/ccrsf-ifx/Software/tools/conda_env4scwf
module load singularity

snakemake -s workflow/Snakefile4test_ext --configfile config4test_3sample.ext.yaml --forceall -j 1 test_sc_rna_default
snakemake -s workflow/Snakefile4test_ext --configfile config4test_3sample.ext.yaml --forceall -j 1 test_sc_vdj_default
snakemake -s workflow/Snakefile4test_ext --configfile config4test_3sample.ext.yaml --forceall -j 1 test_sc_multi_default
