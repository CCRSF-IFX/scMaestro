# Design of Single Cell Pipeline 

`scMaestro` is a workflow wrapper of a set of snakemake workflows. The snakemake workflow component [`SF_sc-smk-wl`](https://github.com/CCRSF-IFX/SF_sc-smk-wl) is used as a submodule of the repo for [workflow wrapper](https://github.com/CCRSF-IFX/scMaestro). With the snakemake workflow as a seperate github repo, the wrappers we designed for internal use ([SF_scMaestro](https://github.com/CCRSF-IFX/SF_scMaestro))(**private repo**) and external use ([scMaetro](https://github.com/CCRSF-IFX/scMaetro)) can share the same snakemake workflow. This separation allows us to open-source our Snakemake workflow together with the wrapper for external users. 

One feature of `scMaestro` is that the snakemake workflow will be copied to the analysis folder. The benefit that this provides a self-contained and reproducible environment for the analysis. 

Another feature is that `cMaestro` relies on singularity. Singularity images will be created at the beginning of snakemake workflow run. This feature again improves the reproducibility of the analysis. 

The singularity-related arguments `use-singularity` and `singularity-args` for snakemake workflow can be found [here](https://github.com/CCRSF-IFX/SF_sc-smk-wl/blob/9d49b8c810baaa91505d88577931bc8902cc06d8/profile/slurm/config.v8%2B.yaml#L11-L12). 

