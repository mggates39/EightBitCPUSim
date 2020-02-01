class Cell:

    def __init__(self, address, label=None, operator=None, operand=None) -> None:
        super().__init__()
        self.address = address
        self.label = label
        self.operator = operator
        self.operand = operand
        self.op_code = None
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
            self.op_code = instructions.lookup_op_code(self.operator)
            if self.operand is not None:
                self.value = self.back_patch_label(self.operand, labels)
                if instructions.is_operand_numeric(self.operator):
                    self.operand = "{}".format(self.value)
                else:
                    self.operand = "({}) ; {}".format(self.value, self.operand)
            else:
                self.value = 0
                self.operand = ''
        else:
            self.value = self.operand

    def get_memory(self):
        if self.op_code is not None:
            mem_value = self.op_code << 4 | (self.value & 0xF)
        else:
            mem_value = self.value & 0xFF

        return mem_value

    def get_listing(self):
        if self.label is None:
            if self.operator is None:
                listing = "{0:02} - ".format(self.address) + " 0b{0:08b}\t".format(
                    self.get_memory()) + "    .byte {}\n".format(self.get_memory())
            else:
                listing = "{0:02} - ".format(self.address) + " 0b{0:08b}\t".format(
                    self.get_memory()) + "    {} {}\n".format(
                    self.operator, self.operand)
        else:
            if self.operator is None:
                listing = "{0:02} - ".format(self.address) + " 0b{0:08b}\t".format(
                    self.get_memory()) + " {}: .byte {}\n".format(self.label, self.get_memory())
            else:
                listing = "{0:02} - ".format(self.address) + " 0b{0:08b}\t".format(
                    self.get_memory()) + " {}: {} {}\n".format(self.label, self.operator, self.operand)

        return listing
