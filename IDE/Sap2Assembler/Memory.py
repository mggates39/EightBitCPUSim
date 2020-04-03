from Sap2Assembler.Segment import MAX_ADDRESS


def get_label_for_address(labels, address):
    label = ""
    for labelTuple in labels:
        if labelTuple[0] == address:
            label = labelTuple[1]
            break

    return label


class Memory:
    def __init__(self) -> None:
        super().__init__()
        self.mem = bytearray(MAX_ADDRESS)

    def set_memory(self, address, memory_array):
        current_address = address
        for value in memory_array:
            if value is not None:
                self.mem[current_address] = value
                current_address += 1

    def get_memory_array(self):
        return self.mem

    def dump(self, labels, code_segment):
        lines = []
        code_cells = {}
        if code_segment is not None:
            code_cells = code_segment.cell_list

        address = 0
        for x in self.mem:
            label = get_label_for_address(labels, address)
            if address < len(code_cells):
                if len(label):
                    lines.append("0x{0:04X},".format(x) + " // {}: {}\n".format(label, x))
                else:
                    lines.append("0x{0:04X},".format(x) + " //   {}\n".format(x))
                # if len(label):
                #     if code_cells[address].operator is not None:
                #         lines.append(
                #             "0x{0:04X},".format(x) + " // {}: {} {}\n".format(label, code_cells[address].operator,
                #                                                               code_cells[address].operand))
                #     else:
                #         lines.append("0x{0:04X},".format(x) + " // {}: {}\n".format(label, x))
                # elif code_cells[address].operator is not None:
                #     lines.append("0x{0:04X},".format(x) + " //   {} {}\n".format(code_cells[address].operator,
                #                                                                  code_cells[address].operand))
                # else:
                #     lines.append("0x{0:04X},".format(x) + " // {}: {}\n".format(label, x))
            else:
                if len(label):
                    lines.append("0x{0:04X},".format(x) + " // {}: {}\n".format(label, x))
                else:
                    lines.append("0x{0:04X},".format(x) + " //   {}\n".format(x))

            address += 1

        return lines
