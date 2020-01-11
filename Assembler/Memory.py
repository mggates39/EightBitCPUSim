
class Memory:
    def __init__(self) -> None:
        super().__init__()
        self.mem = bytearray(16)

    def setMemory(self, address, value):
        self.mem[address] = value

    def getLabel(self,lables, address):
        label = ""
        for labelTuple in lables:
            if labelTuple[0] == address:
                label = labelTuple[1]
                break

        return label

    def dump(self, labels, code_segment):
        code_cells = {}
        if code_segment is not None:
            code_cells = code_segment.cell_list

        address = 0
        for x in self.mem:
            label = self.getLabel(labels, address)
            if address < len(code_cells):
                print("0b{0:08b},".format(x), " //", label, code_cells[address].operator, code_cells[address].operand)
            else:
                print("0b{0:08b},".format(x), " //", label)
            address += 1

