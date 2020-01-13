
class Cell:

    def __init__(self, address, label=None, operator=None, operand=None) -> None:
        super().__init__()
        self.address = address
        self.label = label
        self.operator = operator
        self.operand = operand
        self.opcode = None
        self.value = None

    def backpatch_label(self, operand, labels):
        value = operand
        for label in labels:
            if operand == label[1]:
                value = label[0]
                break

        try:
            value = int(value)
        except ValueError:
            print("ERROR: Lable {} not found.".format(value))
            exit(-3)

        return value

    def assemble(self, labels, instructions):
        if self.operator is not None:
            self.opcode = instructions.lookup_opcode(self.operator)
            if self.operand is not None:
                self.value = self.backpatch_label(self.operand, labels)
                if (self.operator != 'LDI'):
                    self.operand = "({}) ; {}".format(self.value, self.operand)
            else:
                self.value = 0
                self.operand = ''
        else:
            self.value = self.operand

    def get_memory(self):
        if self.opcode is not None:
            memValue = self.opcode << 4 | (self.value & 0xF)
        else:
            memValue = self.value & 0xFF

        return memValue
