class Instructions:
    def __init__(self) -> None:
        super().__init__()
        self.operators = [("NOP", 0),
                          ("LDA", 1),
                          ("ADD", 2),
                          ("SUB", 3),
                          ("STA", 4),
                          ("LDI", 5),
                          ("JMP", 6),
                          ("JC", 7),
                          ("JZ", 8),
                          ("NOP", 9),
                          ("NOP", 10),
                          ("NOP", 11),
                          ("NOP", 12),
                          ("NOP", 13),
                          ("OUT", 14),
                          ("HLT", 15)]

    def lookup_opcode(self, operator):
        op_code = 0
        for o in self.operators:
            if o[0] == operator:
                op_code = o[1]
                break

        return op_code

    def is_operator(self, operator):
        return self.lookup_opcode(operator) != 0
