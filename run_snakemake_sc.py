import argparse
class UniqueStore(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(option_string + " appears several times.")
        setattr(namespace, self.dest, values)

if __name__ == '__main__':
    ## description - Text to display before the argument help (default: none)
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-o', '--output', help='output file', default = "Output_file.tab")

    parser=argparse.ArgumentParser(description='scMastro: ')

    subparsers = parser.add_subparsers(help='sub-command help', dest = 'command')
    parser_rna = subparsers.add_parser("rna", help='Snakemake pipeline for 10x scRNA-seq data')
    parser_rna.add_argument('-f', '--fastqs', metavar='input', nargs = "*",  \
            action = UniqueStore, 
            help='Input file', required=True)
    parser_rna.add_argument('-r', '--reference', metavar='input', \
                      # metavar - A name for the argument in usage messages.
                      help='Input file', required=True)
    parser_rna.add_argument('-p', '--prefix', metavar='prefix', help='Prefix of the tab-delemited')
    options = parser.parse_args()
    dict_cmd = vars(options)
    print("Subcommand is: " + dict_cmd['command'])
    print(options.fastqs)

