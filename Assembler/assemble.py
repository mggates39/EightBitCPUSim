import argparse

from Memory import Memory
from Instructions import Instructions
from Parser import Parser

def assemble(file_name):
    symbols = []
    memory = Memory()
    instructions = Instructions()
    sap1_parser = Parser()

    print("Assemble {}".format(file_name))
    segments = sap1_parser.parse_file(file_name)

    if segments == []:
        print("ERROR: No code found in source file")
        exit(-2)

    # Extract all the lables from the segments to create a symbol table
    for segment in segments:
        for label in segment.labels:
            symbols.append(label)

    for segment in segments:
        segment.assemble(symbols, instructions)

    code_segment = None
    for segment in segments:
        if segment.is_code():
            code_segment = segment
        memory = segment.load_memory(memory)

    memory.dump(symbols, code_segment)


parser = argparse.ArgumentParser(description='Assemble a SAP-1 Assembler file to binary.')
parser.add_argument('--file', dest="file_name", required=True, help='filename to assemble')
args = parser.parse_args()

assemble(args.file_name)