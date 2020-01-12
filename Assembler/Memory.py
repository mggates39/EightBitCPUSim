
class Memory:
    def __init__(self) -> None:
        super().__init__()
        self.mem = bytearray(16)

    def set_memory(self, address, value):
        self.mem[address] = value

    def get_label(self, lables, address):
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
            label = self.get_label(labels, address)
            if address < len(code_cells):
                if len(label):
                    print("0b{0:08b},".format(x), " // {}: {} {}".format(label, code_cells[address].operator, code_cells[address].operand))
                else:
                    print("0b{0:08b},".format(x)," //   {} {}".format(code_cells[address].operator, code_cells[address].operand))
            else:
                print("0b{0:08b},".format(x), " // {}: {}".format(label, x))
            address += 1

