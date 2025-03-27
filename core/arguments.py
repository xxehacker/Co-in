import argparse as ap

def parse_arguments():
    parser = ap.ArgumentParser(
        prog="Co-In",
        description="Co-In is a tool to extract data from a company website and save it in a markdown file.",
        usage="%(prog)s.py -u <url> -o <output> [optional arguments]",
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Enter the company website URL (e.g., google.com)",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Enter the output file name.It's optional. If not provided, the file will be saved with the domain name 'google.com.md'.",
    )
    args = parser.parse_args()

    return args
