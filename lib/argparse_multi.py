import pandas as pd

def multi_conditional_required_flag(args, parser):
    # Read the content of the input file
    df = pd.read_csv(args.library_config)

    # Check if the file contains 'VDJ'
    if df['Type'].str.contains('VDJ').any():
        if not getattr(args, "vdj_ref", None):
            parser.error(": Argument --vdj_ref is required when input file contains 'VDJ' data\n")

    # Check for capture types and require the --feature argument if present
    capture_types = ['Antibody Capture', 'Multiplexing Capture']
    if any(df['Type'].str.contains(capture_type).any() for capture_type in capture_types):
        if not getattr(args, "feature", None):
            parser.error(": Argument --feature is required when input file contains 'Antibody Capture' or 'Multiplexing Capture' data\n")
