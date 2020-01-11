
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

    def dump(self, labels, codeCells):
        address = 0
        for x in self.mem:
            label = self.getLabel(labels, address)
            if address < len(codeCells):
                print("0b{0:08b},".format(x), " //", label, codeCells[address].operator, codeCells[address].operand)
            else:
                print("0b{0:08b},".format(x), " //", label)
            address += 1

