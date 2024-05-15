import os


def write_configfile(args, work_path): 
    with open('config.py', 'w') as f:
        if vars(args)["command"] != 'multirna':
            f.write('unaligned=["%s"]\n' % '","'.join([os.path.abspath(i) for i in args.fa.split(',')]))
            f.write('analysis="%s"\n' % (work_path))
            f.write('ref="%s"\n' % str(args.refgenome))
        if vars(args)["command"]== 'rna':
            if args.expect:
                    f.write('numcells="%s"\n' % str(args.expect))
            if args.force:
                f.write('numcells="%s"\n' % str(args.force)) 
            if args.exclude_introns:
                f.write('include_introns=False\n')
        if args.pipeline == 'pipseq' and args.force:
            f.write('numcells="%s"\n' % str(args.force)) 
        if args.force:
            if not (vars(args)["command"] == 'vdj' or vars(args)["command"] == 'multirna'):
                f.write('forcecells=True\n')
            if args.pipeline == 'atac':
                f.write('numcells=""\n')
        if args.cmo:
            f.write('cmo="%s"\n' % args.cmo)
        

def get_smk_file(pipeline, fullanalysis):
    """_Get the corresponding snakemake file_

    Args:
        pipeline (str): Pipeline name ( e.g. rna, multi, etc) 
        fullanalysis (bool): Whehter full analyisis is needed

    Returns:
        _type_: The path of Snakemake file
    """
    if pipeline == "rna":
        if fullanalysis:
            return "workflow/Snakefile_rna_fullanalysis"
        else:
            return "workflow/Snakefile_rna"
    elif pipeline == "multi":
        return "workflow/Snakefile_multi"
    elif pipeline == "spatial":
        return "workflow/Snakefile_spatial"
    else:
        pass

def get_config_val(config_file):
    """_Get pipeline and fullanalysis_

    Args:
        config_file (_type_): 'config.py' file

    Returns:
        pipeline (str): Pipeline name ( e.g. rna, multi, etc) 
        fullanalysis (bool): Whehter full analyisis is needed
    """
    pipeline, fullanalysis = 'rna', False
    with open(config_file) as fconfig:
        for line in fconfig:
            if line.startswith('pipeline='):
                pipeline = line.rstrip().split('=')[-1].strip('"')
            if line.startswith('fullanalysis='):
                fullanalysis = line.rstrip().split('=')[-1].strip('"')
    return pipeline, fullanalysis