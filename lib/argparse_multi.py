import pandas as pd

def multi_conditional_required_flag(args, parser):
    # Read the content of the input file
    if getattr(args, "vdj_ref", None): 
        df = pd.read_csv(args.library_config)
        # Check if the file contains 'VDJ'
        if df['Type'].str.contains('VDJ').any():
            if not getattr(args, "vdj_ref", None):
                parser.error("argument --vdj_ref is required when input file contains 'VDJ' data")
        capture_types = ['Antibody Capture', 'Multiplexing Capture']

        for capture_type in capture_types:
            if df['Type'].str.contains(capture_type).any():
                if not getattr(args, "feature", None):
                    parser.error(f"argument --feature is required when input file contains '{capture_type}' data")
