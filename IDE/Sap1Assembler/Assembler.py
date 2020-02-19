from Sap1Assembler.Instructions import Instructions
from Sap1Assembler.Memory import Memory
from Sap1Assembler.Parser import Parser


class Assembler:
    def __init__(self, ) -> None:
        super().__init__()
        self.errors = []
        self.sap1_parser = Parser()
        self.memory = None
        self.memory_dump = []
        self.symbols = []

    def assemble_segments(self, segments):
        self.symbols = []
        self.memory = Memory()
        self.memory_dump = []
        instructions = Instructions()
        listing = ""

        if not segments:
            self.errors.append("ERROR: No code found in source code\n")
        else:

            # Extract all the labels from the segments to create a symbol table
            for segment in segments:
                for label in segment.labels:
                    self.symbols.append(label)

            for segment in segments:
                segment.assemble(self.symbols, instructions)
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
            listing += "\n\t.end"

        return listing

    def assemble_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()
        return self.assemble(lines)

    def assemble(self, text):
        segments = self.sap1_parser.parse_strings(text)
        return self.assemble_segments(segments)

    def get_errors(self):
        parse_errors = self.sap1_parser.get_errors()
        for error in parse_errors:
            self.errors.append(error)
        return self.errors

    def get_memory_dump(self):
        return self.memory_dump

    def get_memory(self):
        return self.memory
