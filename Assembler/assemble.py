import argparse

from Memory import Memory
from Instructions import Instructions
from Parser import Parser

def assemble(file_name):
    labels = []
    segments = []
    m = Memory()
    i = Instructions()
    p = Parser()

    print("Assemble {}".format(file_name))
    segments = p.parseFile(file_name)

    for segment in segments:
        for label in segment.labels:
            labels.append(label)

    for segment in segments:
        segment.assemble(labels, i)

    for segment in segments:
        if segment.isCode():
            code_segment = segment
        m = segment.loadMemory(m)

    m.dump(labels, code_segment.cell_list)

parser = argparse.ArgumentParser(description='Assemble a SAP-1 Assembler file to binary.')
parser.add_argument('--file', dest="file_name", required=True, help='filename to assemble')
args = parser.parse_args()

assemble(args.file_name)