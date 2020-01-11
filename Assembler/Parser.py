from Segment import Segment

class Parser:
    def __init__(self) -> None:
        super().__init__()


    def parse_file(self, file_name):
        segments = []

        code_segment = Segment(0, 'C')
        code_segment.add_instruction("top", "LDA", "x")
        code_segment.add_instruction(None, "SUB", "One")
        code_segment.add_instruction(None, "JC", "continue")
        code_segment.add_instruction(None, "LDA", "product")
        code_segment.add_instruction(None, "OUT")
        code_segment.add_instruction(None, "HLT")
        code_segment.add_label("continue")
        code_segment.add_instruction(None, "STA", "x")
        code_segment.add_instruction(None, "LDA", "product")
        code_segment.add_instruction(None, "ADD", "y")
        code_segment.add_instruction(None, "STA", "product")
        code_segment.add_instruction(None, "JMP", "top")
        segments.append(code_segment)

        data_segment = Segment(12, 'D')
        data_segment.add_byte("One", 1)
        data_segment.add_label("product")
        data_segment.add_byte(None, 0)
        data_segment.add_byte("x", 3)
        data_segment.add_byte("y", 29)
        segments.append(data_segment)

        if code_segment.overlaps(data_segment):
            print("ERROR: Segments overlap")
            exit(-1)

        return segments