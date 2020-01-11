import argparse

from Memory import Memory
from Instructions import Instructions
from Parser import Parser

def assemble(file_name):
    labels = []
    segments = []
    memory = Memory()
    instructions = Instructions()
    sap1_parser = Parser()

    print("Assemble {}".format(file_name))
    segments = sap1_parser.parseFile(file_name)

    # Extract all the lables from the segments to create a symbol table
    for segment in segments:
        for label in segment.labels:
            labels.append(label)

    for segment in segments:
        segment.assemble(labels, instructions)

    code_segment = None
    for segment in segments:
        if segment.isCode():
            code_segment = segment
        memory = segment.loadMemory(memory)

    memory.dump(labels, code_segment)


parser = argparse.ArgumentParser(description='Assemble a SAP-1 Assembler file to binary.')
parser.add_argument('--file', dest="file_name", required=True, help='filename to assemble')
args = parser.parse_args()

assemble(args.file_name)