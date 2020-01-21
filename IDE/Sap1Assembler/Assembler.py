from Sap1Assembler.Instructions import Instructions
from Sap1Assembler.Memory import Memory
from Sap1Assembler.Parser import Parser


class Assembler:
    def __init__(self, ) -> None:
        super().__init__()
        self.sap1_parser = Parser()

    @staticmethod
    def assemble_segments(segments):
        symbols = []
        memory = Memory()
        instructions = Instructions()

        if not segments:
            print("ERROR: No code found in source file")
            exit(-2)

        # Extract all the labels from the segments to create a symbol table
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

        return memory.dump(symbols, code_segment)

    def assemble_file(self, file_name):
        print("Assemble {}".format(file_name))
        segments = self.sap1_parser.parse_file(file_name)

        self.assemble_segments(segments)

    def assemble(self, text):
        print("Assemble {}".format(text))
        segments = self.sap1_parser.parse_strings(text)

        return self.assemble_segments(segments)
