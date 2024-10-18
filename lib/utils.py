import os


def write_configfile(args, work_path): 
    args.pipeline = vars(args)["command"]
    with open('config.py', 'w') as f:
        if vars(args)["command"] != 'multirna':
            f.write('unaligned=["%s"]\n' % '","'.join([os.path.abspath(i) for i in args.fastqs]))
            f.write('analysis="%s"\n' % (work_path))
            f.write('ref="%s"\n' % str(args.genome))
        if vars(args)["command"] == 'rna':
            if args.expect:
                    f.write('numcells="%s"\n' % str(args.expect))
            if args.force:
                f.write('numcells="%s"\n' % str(args.force)) 
            if args.exclude_introns:
                f.write('include_introns=False\n')
        if args.pipeline == 'pipseq' and args.force:
            f.write('numcells="%s"\n' % str(args.force)) 
        if hasattr(args, 'cmo') and args.cmo:
            f.write('cmo="%s"\n' % args.cmo)
        if args.pipeline == 'fb':
            f.write('libraries=""\n')
            f.write('features=""\n')
        #if args.pipeline == 'multirna':
        #    f.write('label = ""\n')
        if args.pipeline == 'multiome':
            f.write(f'libraries="{args.library_config}"\n')
            if args.exclude_introns:
                f.write('include_introns=False\n')
        if args.pipeline == 'multi':
            f.write(f'libraries="{args.library_config}"\n')
            #if args.expect:
            #    f.write('numcells="%s"\n' % ','.join([str(args.expect)] * int(len(samples)/2)))
            #if args.force:
            #    f.write('numcells="%s"\n' % ','.join([str(args.force)] * int(len(samples)/2)))
            #if args.exclude_introns:
            #    f.write('include_introns=False\n')
            #if args.count:
            #    f.write('count=True\n')
            f.write("#inner_enrichment_primers=<path>: needed when detecting gamma-delta chains or studying non-human-mouse species\n")
        if args.pipeline == 'vdj':
            if args.chain == "TR" or  args.chain == "TR":
                f.write('chain="%s"\n' % args.chain)
        if args.pipeline == "fixedrna":
            if args.singleplex == False and args.multiplex == None:
                sys.exit("\nEither --singleplex or --multiplex <multiplexing.csv> is required for FRP data\n")
            if args.singleplex and args.multiplex != None:
                sys.exit("\nOnly one of them is required for FRP data: --singleplex and --multiplex <multiplexing.csv>\n")
            f.write(f'libraries="{args.library_config}"\n')
            if args.multiplex != None: 
                f.write(f'multiplex="{args.multiplex}"\n')
            f.write(f'probe_set="{args.probe_set}"\n')
        if args.pipeline == "spatial":
            f.write('images="%s"\n' % args.images)
            f.write('spatial_method="%s"\n' % args.spatial_method)
        f.write('pipeline="%s"\n' % str(args.pipeline))
        if hasattr(args, 'chemistry') and args.chemistry != None:
            f.write('chemistry="%s"\n' % args.chemistry) 
        if args.pipeline != "fixedrna":
            f.write("#aggregate=False # Recommended value to set as 'False' when 1) three are too many samples (>10); 2) no donor and origin information provided for VDJ libraries;\n")
        else:
            f.write("aggregate=False # Default value for fixed RNA profiling data")

def get_smk_file(pipeline, fullanalysis = None):
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
    elif pipeline == "vdj":
        return "workflow/Snakefile_vdj"
    elif pipeline == "atac":
        return "workflow/Snakefile_atac"
    elif pipeline == "multiome":
        return "workflow/Snakefile_multiome"
    elif pipeline == "fixedrna":
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

def prep_ref(args):
    with open('reference.py', 'w') as f:
        f.write(f'''
import config
genomename = ""
if config.ref == "{args.genome}":
''')
        f.write(f'    genomename = "{args.genome}"\n')
        if args.pipeline == 'rna' or args.pipeline == 'multi':
            f.write(f'    transcriptome = "{args.reference}"\n')
            if getattr(args, 'vdj_ref', None):
                f.write(f'    vdj_reference = "{args.vdj_ref}"\n')
        if args.pipeline == 'atac':
            f.write(f'    atac_reference = "{args.reference}"\n')
        if args.pipeline == 'multiome':
            f.write(f'    arc_reference = "{args.reference}"\n')
        if args.pipeline == 'vdj':
            f.write(f'    vdj_reference = "{args.reference}"\n')
        if args.pipeline == 'pipseq':
            f.write(f'    pipseq_reference = "{args.reference}"\n')

##!def get_smk_file(pipeline, fullanalysis):
##!    if pipeline == "rna":
##!        if fullanalysis:
##!            return "workflow/Snakefile_rna_fullanalysis"
##!        else:
##!            return "workflow/Snakefile_rna"
##!    elif pipeline == "multi":
##!        return "workflow/Snakefile_multi"
##!    elif pipeline == "spatial":
##!        return "workflow/Snakefile_spatial"
##!    elif pipeline == "vdj":
##!        return "workflow/Snakefile_vdj"
##!    elif pipeline == "multiome":
##!        return "workflow/Snakefile_multiome"
##!    elif pipeline == "atac":
##!        return "workflow/Snakefile_atac"
##!    elif pipeline == "nopipe":
##!        return "workflow/Snakefile_nopipe"
##!    elif pipeline == "pipseq":
##!        return "workflow/Snakefile_pipseq"
##!    elif pipeline == "multirna":
##!        return "workflow/Snakefile_multirna"
##!    else:
##!        pass
