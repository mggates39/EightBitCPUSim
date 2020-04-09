from Sap3Assembler.Instructions import Instructions
from Sap3Assembler.Memory import Memory
from Sap3Assembler.NumericStringParser import NumericStringParser
from Sap3Assembler.Parser import Parser


class Assembler:
    def __init__(self, ) -> None:
        super().__init__()
        self.instructions = Instructions()
        self.errors = []
        self.sap3_parser = Parser(self.instructions)
        self.memory = None
        self.memory_dump = []
        self.symbols = []
        self.labels = {}
        self.equates = {}
        self.np = NumericStringParser()

    def assemble_segments(self, segments):
        self.symbols = []
        self.labels = {}
        self.memory = Memory()
        self.memory_dump = []
        listing = ""

        if not segments:
            self.errors.append("ERROR: No code found in source code\n")
        else:
            # Extract all the valid labels, those that have integer values
            # si we can then parse the ones that don't

            all_done = True
            for segment in segments:
                for label in segment.labels:
                    if type(label[0]) is int:
                        self.labels[label[1]] = label[0]
                    else:
                        all_done = False

            # while there were invalid labels
            while not all_done:
                all_done = True
                self.np.set_labels(self.labels)
                for segment in segments:
                    for label in segment.labels:
                        if label[1] not in self.labels:
                            if type(label[0]) is not int:
                                # Parse the value and save the label and equate record
                                value = int(self.np.eval(label[0]))
                                self.labels[label[1]] = value
                                self.equates[label[1]] = label[0]
                                self.np.set_labels(self.labels)
                                all_done = False


            # Extract all the labels from the segments to create a full and correct symbol table from parsed labels
            for segment in segments:
                for label in segment.labels:
                    if label[1] in self.labels:
                        self.symbols.append((self.labels[label[1]], label[1]))

            self.np.set_labels(self.labels)

            for segment in segments:
                segment.assemble(self.np)
                segment_errors = segment.get_errors()
                for error in segment_errors:
                    self.errors.append(error)

            code_segment = None
            for segment in segments:
                if segment.is_code():
                    code_segment = segment
                self.memory = segment.load_memory(self.memory)

            self.memory_dump = self.memory.dump(self.symbols, code_segment)

            for segment in segments:
                listing += segment.get_listing()

            # Add the leftover equate statements
            listing += "\n"
            for label in self.equates:
                listing += "                               {:<10s}".format(label + ':')
                listing += " EQU {0}".format(self.equates[label])
                listing += "\n"

            listing += "\n\tEND\n\n"

            listing += 'Labels:\n'
            lc = 0
            for symbol in self.symbols:
                listing += ("{0} - 0x{1:04X}\t".format(symbol[1], symbol[0]))
                lc += 1
                if lc > 3:
                    listing += '\n'
                    lc = 0
            listing += '\n'

        return listing

    def assemble_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()
        return self.assemble(lines)

    def assemble(self, text):
        segments = self.sap3_parser.parse_strings(text)
        return self.assemble_segments(segments)

    def get_errors(self):
        parse_errors = self.sap3_parser.get_errors()
        for error in parse_errors:
            self.errors.append(error)
        return self.errors

    def get_memory_dump(self):
        return self.memory_dump

    def get_memory(self):
        return self.memory
