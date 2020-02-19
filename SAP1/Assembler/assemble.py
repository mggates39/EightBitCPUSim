import argparse

from Assembler import Assembler


def assemble(file_name):
    a = Assembler()
    listing, memory_dump = a.assemble_file(file_name)
    errors = a.get_errors()

    print(listing)

    if len(errors):
        print("\nErrors:")
        for line in errors:
            print(line[:-1])

    print("")

    for line in memory_dump:
        print(line[:-1])

parser = argparse.ArgumentParser(description='Assemble a SAP-1 Assembler file to binary.')
parser.add_argument('--file', dest="file_name", required=True, help='filename to assemble')
args = parser.parse_args()

assemble(args.file_name)
