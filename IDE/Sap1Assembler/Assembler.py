from Sap1Assembler.Instructions import Instructions
from Sap1Assembler.Memory import Memory
from Sap1Assembler.Parser import Parser


class Assembler:
    def __init__(self, ) -> None:
        super().__init__()
        self.errors = []
        self.sap1_parser = Parser()

    def assemble_segments(self, segments):
        symbols = []
        listing = ""
        memory_dump = []
        memory = Memory()
        instructions = Instructions()

        if not segments:
            self.errors.append("ERROR: No code found in source code\n")
        else:

            # Extract all the labels from the segments to create a symbol table
            for segment in segments:
                for label in segment.labels:
                    symbols.append(label)

            for segment in segments:
                segment.assemble(symbols, instructions)
                segment_errors = segment.get_errors()
                for error in segment_errors:
                    self.errors.append(error)

            code_segment = None
            for segment in segments:
                if segment.is_code():
                    code_segment = segment
                memory = segment.load_memory(memory)

            memory_dump = memory.dump(symbols, code_segment)

            for segment in segments:
                listing += segment.get_listing()
            listing += "\n\t.end"
        return listing, memory_dump

    def assemble_file(self, file_name):
        segments = self.sap1_parser.parse_file(file_name)

        return self.assemble_segments(segments)

    def assemble(self, text):
        segments = self.sap1_parser.parse_strings(text)

        return self.assemble_segments(segments)

    def get_errors(self):
        parse_errors = self.sap1_parser.get_errors()
        for error in parse_errors:
            self.errors.append(error)
        return self.errors
