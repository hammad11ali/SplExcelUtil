from parser import parse_spl_file
from excel_export import export_to_excel
import os
import argparse
from utils import log, init_log
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert a spool file containing multiple query results into Excel file(s).'
    )

    parser.add_argument(
        'input_file',
        help='Path to the input spool file (e.g., cl_accounts.spl).'
    )

    parser.add_argument(
        '-d', '--destination',
        help=(
            'Destination file name (for single Excel) or folder name (for multiple files).\n'
            'If not provided, defaults to:\n'
            '  - <input_filename>.xlsx (if creating a single Excel file)\n'
            '  - <input_filename>/ folder (if creating multiple Excel files)'
        )
    )

    parser.add_argument(
        '-s', '--separate',
        action='store_true',
        help='Create a separate Excel file for each query result instead of separate sheets in one file.'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose mode. Shows detailed output of each processing step.'
    )

    parser.add_argument(
        '-st', '--showstats',
        action='store_true',
        help='Include a summary sheet (or file) listing each query and its row count.'
    )

    return parser.parse_args()


def main(input_file, destination, separate, verbose, showstats):
    # Input and output paths

    
    # Parse the SPL file
    log('Main', f"Parsing {input_file}...", verbose, mandatory=True)
    results = parse_spl_file(input_file, verbose_flag=verbose, )
    
    # Export to Excel
    log('Main', f"Found and parsed {len(results)} queries in {input_file}.", verbose, mandatory=True)
    log('Main', f"Initiating export to destination: {destination}...", verbose, mandatory=True)
    
    export_to_excel(results, destination, separate, verbose, showstats)
    log("Main", "Export completed.", verbose, mandatory=True)

if __name__ == "__main__":
    args = parse_arguments()
    # Derive default destination if not provided
    if not args.destination:
        base = os.path.splitext(os.path.basename(args.input_file))[0]
        args.destination = base if args.separate else f"{base}.xlsx"
    if args.verbose:
        init_log(args.input_file)
    try:
        main(
            input_file=args.input_file,
            destination=args.destination,
            separate=args.separate,
            verbose=args.verbose,
            showstats=args.showstats
        )
    except Exception as e:
        log("Main", f"An error occurred: {e}", args.verbose, mandatory=True)
        raise