from Segment import Segment

class Parser:
    def __init__(self) -> None:
        super().__init__()


    def parseFile(self, file_name):
        segments = []

        code_segment = Segment(0, 'C')
        code_segment.addInstruction("top", "LDA", "x")
        code_segment.addInstruction(None, "SUB", "One")
        code_segment.addInstruction(None, "JC", "continue")
        code_segment.addInstruction(None, "LDA", "product")
        code_segment.addInstruction(None, "OUT")
        code_segment.addInstruction(None, "HLT")
        code_segment.addLabel("continue")
        code_segment.addInstruction(None, "STA", "x")
        code_segment.addInstruction(None, "LDA", "product")
        code_segment.addInstruction(None, "ADD", "y")
        code_segment.addInstruction(None, "STA", "product")
        code_segment.addInstruction(None, "JMP", "top")
        segments.append(code_segment)

        data_segment = Segment(12, 'D')
        data_segment.addByte("One", 1)
        data_segment.addLabel("product")
        data_segment.addByte(None, 0)
        data_segment.addByte("x", 3)
        data_segment.addByte("y", 29)
        segments.append(data_segment)

        return segments