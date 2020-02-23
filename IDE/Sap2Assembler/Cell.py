class Cell:

    def __init__(self, line_number, address, label=None, operator=None, first_operand=None, second_operand=None) -> None:
        super().__init__()
        self.line_number = line_number
        self.address = address
        self.label = label
        self.operator = operator
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.op_code = None
        self.first_value = None
        self.second_value = None
        self.good = True

    def back_patch_label(self, operand, labels):
        error = ""
        value = operand
        for label in labels:
            if operand == label[1]:
                value = label[0]
                break

        try:
            value = int(value)
        except ValueError:
            error = "ERROR: Label {} not found at address {}.\n".format(value, self.address)
            self.good = False

        return value, error

    def assemble(self, labels, instructions):
        error = ""
        if self.operator is not None:
            self.op_code = instructions.lookup_op_code(self.operator)
            if self.op_code == -1:
                error = "ERROR: Unknown operator {} at {}.\n".format(self.operator, self.address)
                self.op_code = 0
                self.first_value = 0
                self.first_operand = ''
            else:
                if self.first_operand is not None:
                    self.first_value, error = self.back_patch_label(self.first_operand, labels)
                    if instructions.is_operand_numeric(self.operator):
                        self.first_operand = "{}".format(self.first_value)
                    else:
                        self.first_operand = "({}) ; {}".format(self.first_value, self.first_operand)
                else:
                    self.first_value = 0
                    self.first_operand = ''
        else:
            self.first_value = self.first_operand
        return error

    def get_memory(self):
        mem_value = 0
        if self.good:
            if self.op_code is not None:
                mem_value = self.op_code << 4 | (self.first_value & 0xF)
            else:
                mem_value = self.first_value & 0xFF

        return mem_value

    def get_listing(self):
        listing = "{0:05} - 0x{0:04X}: ".format(self.line_number, self.address)

        if self.label is not None:
            listing += "{:<10s}".format(self.label+':')
        else:
            listing += "{:<10s}".format(' ')

        if self.operator is None:
            listing += " .byte {}".format(self.get_memory())
        else:
            listing += " {}".format(self.operator)
            if self.first_operand is not None:
                listing += " {}".format(self.first_operand)
            if self.second_operand is not None:
                listing += ", {}".format(self.second_operand)

        listing += "\n"
        
        return listing
