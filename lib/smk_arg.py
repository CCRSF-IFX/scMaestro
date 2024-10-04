import subprocess
import os
import sys
from .utils import get_config_val, get_smk_file

def smk_rerun_dryrun_unlock(cmd, subparser):
    subcommands = [i for i in subparser.choices if i not in ['rerun', 'dryun', 'unlock']]
    if not os.path.exists("config.py") or not os.path.isfile("config.py"):
        sys.exit(f'File "config.py" not found, please make sure you have run one of'
                 f' the subcomands :{", ".join(subcommands)}\n')
    pipeline, fullanalysis = get_config_val("config.py")
    smk_file = get_smk_file(pipeline, fullanalysis)
    smk_output = subprocess.check_output(f'snakemake -s {smk_file} -np', shell=True)
    if cmd == 'rerun':
        ('CONFIG FILE:')
        with open('config.py') as f:
            print(f.read())
            submit = input('Submit now? (y/n): ')
            while submit.lower() not in ['y', 'n']:
                submit = input('Please answer yes(y) or no(n): ')
            if submit.lower() == 'y':
                subprocess.check_output('sbatch submit.sh', shell=True)
                print("Submitted snakemake rerun in directory")
        if cmd == 'unlock':
                subprocess.check_output(f'snakemake -s {smk_file} --unlock', shell=True)