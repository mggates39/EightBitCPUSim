class Cell:

    def __init__(self, address, label=None, operator=None, operand=None) -> None:
        super().__init__()
        self.address = address
        self.label = label
        self.operator = operator
        self.operand = operand
        self.opcode = None
        self.value = None

    @staticmethod
    def back_patch_label(operand, labels):
        value = operand
        for label in labels:
            if operand == label[1]:
                value = label[0]
                break

        try:
            value = int(value)
        except ValueError:
            print("ERROR: Label {} not found.".format(value))
            exit(-3)

        return value

    def assemble(self, labels, instructions):
        if self.operator is not None:
            self.opcode = instructions.lookup_opcode(self.operator)
            if self.operand is not None:
                self.value = self.back_patch_label(self.operand, labels)
                if self.operator != 'LDI':
                    self.operand = "({}) ; {}".format(self.value, self.operand)
            else:
                self.value = 0
                self.operand = ''
        else:
            self.value = self.operand

    def get_memory(self):
        if self.opcode is not None:
            mem_value = self.opcode << 4 | (self.value & 0xF)
        else:
            mem_value = self.value & 0xFF

        return mem_value
