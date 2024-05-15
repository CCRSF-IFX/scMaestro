import argparse
import glob
import itertools
import logging as sflog
import os
import re
import subprocess
sflog.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=sflog.DEBUG)

from lib.utils import get_smk_file, write_configfile, get_config_val

class UniqueStore(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(option_string + " appears several times.")
        setattr(namespace, self.dest, values)

if __name__ == '__main__':
    ## description - Text to display before the argument help (default: none)

    parent_parser = argparse.ArgumentParser(add_help=False)  
    parent_parser.add_argument('-f', '--fastqs', metavar='FASTQPATH', nargs = "*",  \
            action = UniqueStore, required=True, 
            help='Path(s) to fastq files, multiple paths can be provided together. eg. "-f path1 path2"')
    parent_parser.add_argument('-r', '--reference', metavar='REFERENCE FOLDER', 
            help='Reference genome folder for alignment', required=True)
    parent_parser.add_argument('-g', '--genome', 
            help='Genome build, e.g. "hg38", "mm10"', required=True)
    parent_parser.add_argument("-n", "--dryrun", action="store_true", help="dry run") 
    parent_parser.add_argument("--rerun", action="store_true",
            help="dry run then prompt for submitting jobs that need to be rerun")
    parent_parser.add_argument("--unlock", action="store_true",
            help="unlock working directory")

    parent_parser_fa = argparse.ArgumentParser(add_help=False) 
    parent_parser_fa.add_argument("--fullanalysis", action="store_true",
        help="Run full analysis pipeline")
    
    parent_parser_cellnum = argparse.ArgumentParser(add_help=False) 
    group_cell_number = parent_parser_cellnum.add_mutually_exclusive_group()
    group_cell_number.add_argument("--force", type=int,
        help="Run Cell Ranger with --force-cell ")
    group_cell_number.add_argument("--expect", type=int,
        help="Run Cell Ranger with --expect-cells")
    parent_parser_cellnum.add_argument("--exclude-introns", action="store_true",
        help="Exclude intronic reads in count. To maximize sensitivity for \
                whole transcriptome 3’/5’ Single Cell Gene Expression and 3’ \
                Cell Multiplexing experiments, introns will be included in \
                the analysis by default for cellranger (>v7.0.0) count and multi. ") 
    
    parent_parser_vdjchain = argparse.ArgumentParser(add_help=False)
    parent_parser_vdjchain.add_argument("--chain", default="auto", choices=['auto', 'TR', 'IG'], 
        help="Force the analysis to be carried out for a particular chain type.")

    parser = argparse.ArgumentParser(description='scMastro: comprehensive workflow for processing single cell sequencing data')
    subparsers = parser.add_subparsers(help='sub-command help', dest = 'command')
    ## rna pipeline
    parser_rna = subparsers.add_parser("rna", 
        parents = [parent_parser, parent_parser_fa, parent_parser_cellnum], 
        help='Snakemake pipeline for 10x scRNA-seq data')
    ## multi pipeline
    parser_multi = subparsers.add_parser("multi", 
        parents = [parent_parser, parent_parser_vdjchain], 
        help='Snakemake pipeline for 10x CellRanger multi analysis')
    parser_multi.add_argument("--cmo", action="store_true",
        help="CMO information will be used for multi analysis")
    parser.add_argument("--count", action="store_true",
        help="Run cellranger count for projects with HTO libraries \
                with more 10 individuals mixed. ")
    
    parser_vdj = subparsers.add_parser("vdj", 
        parents = [parent_parser, parent_parser_vdjchain], 
        help='Snakemake pipeline for 10x VDJ data')
    
    parser_multiome = subparsers.add_parser("multiome", 
        parents = [parent_parser], 
        help='Snakemake pipeline for 10x Multiome ATAC + GEX data')
    
    parser_spatial = subparsers.add_parser("spatial", 
        parents = [parent_parser], 
        help='Snakemake pipeline for 10x spatial data')
    parser_spatial.add_argument("--images", metavar="images",
        action = "store", type=str, 
        help="Metadata for image information. [Required if spatial pipeline is used]")
    spatial_methods = ["cytassist_v1", "cytassist_v2", "non_cytassist"]
    parser_spatial.add_argument("--spatial-method", 
        metavar=f"spatial_method {spatial_methods}", 
        type=str, choices = spatial_methods,
        help="""Specify the method used for spatial transcriptomics analysis. 
              Options:                                                      
              - 'cytassist_v1': Employ Cytassist method using probe set v1    
              - 'cytassist_v2': Employ Cytassist method using probe set v2     
              - 'non_cytassist': Employ non-Cytassist method capturing  polyA mRNAs""")
    
    args = parser.parse_args()
    dict_cmd = vars(args)
    sflog.info("Subcommand is: " + dict_cmd['command'])
    sflog.info(args)
    if args.dryrun or args.rerun or args.unlock:
        pipeline, fullanalysis = get_config_val("config.py")
        smk_file = get_smk_file(pipeline, fullanalysis)
        sflog.debug(smk_file)
        smk_output = subprocess.check_output(f'snakemake -s {smk_file} -np', shell=True)
        if args.rerun:
            sflog.info('CONFIG FILE:')
            with open('config.py') as f:
                print(f.read())
            submit = input('Submit now? (y/n): ')
            while submit.lower() not in ['y', 'n']:
                submit = input('Please answer yes(y) or no(n): ')
            if submit.lower() == 'y':
                subprocess.check_output('sbatch submit.sh', shell=True)
                sflog.info("Submitted snakemake rerun in directory")
        if args.unlock:
                subprocess.check_output(f'snakemake -s {smk_file} --unlock', shell=True)
    else:
        work_path = os.getcwd()
        os.chdir(work_path)
        sample = list(set([os.path.basename(file).split('.')[0] for file in list(itertools.chain.from_iterable([glob.glob(i + '/*') for i in args.fastq_path.split(',')]))]))
        samps = []
        for item in sample:
            if len(re.findall(r"(\S*)_S\d+_L0\d{2}_[RI]", item)) > 0:
              samps.append(re.findall(r"(\S*)_S\d+_L0\d{2}_[RI]", item)[0])
            else:
              samps.append(item)
        samples = list(set(s.replace('Sample_', '') for s in set(samps)))
        samples = sorted(samples)
        write_configfile(args)