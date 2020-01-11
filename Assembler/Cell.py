
class Cell:

    def __init__(self, address, label=None, operator=None, operand=None) -> None:
        super().__init__()
        self.address = address
        self.label = label
        self.operator = operator
        self.operand = operand
        self.opcode = None
        self.value = None

    def processLabel(self, operand, labels):
        value = operand
        for label in labels:
            if operand == label[1]:
                value = label[0]
                break
        return value

    def assemble(self, labels, instructions):
        if self.operator is not None:
            self.opcode = instructions.lookupOpcode(self.operator)
            if self.operand is not None:
                self.value = self.processLabel(self.operand, labels)
                self.operand = "<{}> # {}".format(self.value, self.operand)
            else:
                self.value = 0
                self.operand = ''
        else:
            self.value = self.operand

    def getMemory(self):
        if self.opcode is not None:
            memValue = self.opcode << 4 | (self.value & 0xF)
        else:
            memValue = self.value & 0xFF

        return memValue
