
import sys
import os
import csv
try:
    import orjson as json
except:
    import json


def get_input_stream():
    """
    If first paramter is - use standard in, if it's a existing
    file, open an use that
    Return a stream (or None) for processing.
    """
                                      
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        if input_filename == '-':
            if not sys.stdin.isatty():
                return sys.stdin    
        if os.path.isfile(input_filename):
            return open(input_filename, 'r')
    return None

def get_parameter_value(label):
    """
    Look for labelled parameters in the command line, the pattern is:
        -a value
    Where '-a' is the label, and 'value' is the returned value.
    """
    if label in sys.argv:
        idx = sys.argv.index(label)
        if (idx + 1) < len(sys.argv):
            return sys.argv[idx + 1]
    return None

# Initialize variables
verbose      = '--verbose' in sys.argv or '-v' in sys.argv
 # be lenient on people asking for help
show_help    = '-?' in sys.argv or '-h' in sys.argv or '--help' in sys.argv
no_headers   = '-no' in sys.argv
out_file     = get_parameter_value('-o')
input_stream = get_input_stream()

# if help requested, display help and exit with no error
if show_help:
    print("Usage: trosi [FILE] [-o OUTPUTFILE] [--verbose] [--help]")
    print("convert INPUTFILE to a jsonl formatted file")
    print("Example: trosi data.csv -o data.jsonl")
    print()
    print("  FILE\t\tfile to convert")
    print("  -o\t\tfile to save to")
    print("  -v, --verbose\tflag to increase the amount of logging")
    print("  -h, --help\tdisplay this help text and exit")
    print()
    print("When FILE is -, standard input in read.")
    sys.exit(0)

# if we have nothing to processes, display an error and how to get help
if not input_stream:
    print("No input specified.")
    print(f"Try '{sys.argv[0]} --help' for usage information.")
    sys.exit(1)

# if we have nothing to processes, display an error and how to get help
if not out_file:
    print("No output file specified.")
    print(f"Try '{sys.argv[0]} --help' for usage information.")
    sys.exit(1)

with open(out_file, 'w', encoding='utf8') as of:

    csv_reader = csv.reader(input_stream)
    headers = next(csv_reader)  # read the reader row
    # Iterate over each row in the csv using reader object
    counter = 0
    for counter, row in enumerate(csv_reader):
        # row variable is a list that represents a row in csv
        of.write(json.dumps(dict(zip(headers, row))).decode() + '\n')

if counter > 0:
    counter += 1

print(f"written {counter} lines")