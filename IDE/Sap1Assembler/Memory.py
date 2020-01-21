def get_label(labels, address):
    label = ""
    for labelTuple in labels:
        if labelTuple[0] == address:
            label = labelTuple[1]
            break

    return label


class Memory:
    def __init__(self) -> None:
        super().__init__()
        self.mem = bytearray(16)

    def set_memory(self, address, value):
        self.mem[address] = value

    def dump(self, labels, code_segment):
        lines = []
        code_cells = {}
        if code_segment is not None:
            code_cells = code_segment.cell_list

        address = 0
        for x in self.mem:
            label = get_label(labels, address)
            if address < len(code_cells):
                if len(label):
                    if code_cells[address].operator is not None:
                        print("0b{0:08b},".format(x)," // {}: {} {}".format(label, code_cells[address].operator, code_cells[address].operand))
                        lines.append("{0:02} - ".format(address) +" 0b{0:08b}\t".format(x) + " {}: {} {}\n".format(label, code_cells[address].operator, code_cells[address].operand))
                    else:
                        print("0b{0:08b},".format(x), " // {}: {}".format(label, x))
                        lines.append(
                            "{0:02} - ".format(address) + " 0b{0:08b}\t".format(x) + " {}: .byte {}\n".format(label, x))
                elif code_cells[address].operator is not None:
                    print("0b{0:08b},".format(x),
                          " //   {} {}".format(code_cells[address].operator, code_cells[address].operand))
                    lines.append("{0:02} - ".format(address) + " 0b{0:08b}\t".format(x) + "    {} {}\n".format(
                        code_cells[address].operator, code_cells[address].operand))
                else:
                    print("0b{0:08b},".format(x), " // {}: {}".format(label, x))
                    lines.append("{0:02} - ".format(address) + " 0b{0:08b}\t".format(x) + " {}: .byte {}\n".format(label, x))
            else:
                if len(label):
                    print("0b{0:08b},".format(x), " // {}: {}".format(label, x))
                    lines.append("{0:02} - ".format(address) + " 0b{0:08b}\t".format(x) + " {}: .byte {}\n".format(label, x))
                else:
                    print("0b{0:08b},".format(x), " //   {}".format(x))
                    lines.append("{0:02} - ".format(address) + " 0b{0:08b}\t".format(x) + "    .byte {}\n".format(x))

            address += 1

        return lines