class Cell:

    def __init__(self, line_number, address, label=None, operator=None, first_operand=None,
                 second_operand=None, data_size=0, reserved_space=0) -> None:
        super().__init__()
        self.line_number = line_number
        self.address = address
        self.label = label
        self.operator = operator
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.data_size = data_size
        self.reserved_space = reserved_space
        self.op_code = None
        self.first_value = None
        self.second_value = None
        self.memory = [None, None, None]
        self.real_operator = None
        self.size = 0
        self.good = True

    def get_size(self):
        return self.size

    def back_patch_label(self, operand, np):
        error = ""
        value = np.eval(operand)

        try:
            value = int(value)
        except ValueError:
            error = "ERROR: Label {} not found at line {}.\n".format(value, self.line_number)
            self.good = False

        return value, error

    def calculate_size(self, instructions):
        if self.reserved_space != 0:
            self.size = self.reserved_space
        else:
            self.size = 1
            if self.operator is not None:
                mnemonic = instructions.get_mnemonic(self.operator)
                if mnemonic is not None:
                    self.size = mnemonic["bytes"]
            else:
                self.size = self.data_size

    def assemble_pass_one(self, instructions):
        error = ""
        if self.operator is not None:
            self.op_code, real_operator = instructions.lookup_op_code(self.operator, self.first_operand,
                                                                      self.second_operand)
            if self.op_code == -1:
                error = "ERROR: Unknown operator '{}' at {}.\n".format(self.operator, self.line_number)
                self.op_code = 0
                self.first_value = None
                self.second_value = None
            elif self.op_code == -2:
                error = "ERROR: Unknown operand {} {},{} at {}.\n".format(self.operator, self.first_operand,
                                                                          self.second_operand, self.line_number)
                self.op_code = 0
                self.first_value = None
                self.second_value = None

            else:
                self.size = real_operator["bytes"]
                self.real_operator = real_operator["operator"]
        else:
            if self.reserved_space != 0:
                self.size = self.reserved_space
            else:
                self.size = self.data_size

        return error

    def assemble_pass_two(self, instructions, np):
        error = ""
        if self.operator is not None:
            if not instructions.is_operand_one_none(self.real_operator):
                if self.first_operand is not None:
                    if instructions.is_operand_one_memory(self.real_operator):
                        value, error = self.back_patch_label(self.first_operand, np)
                        if self.good:
                            self.first_value = value & 0xFF
                            self.second_value = (value >> 8) & 0xFF
                            # self.first_operand = "(0x{0:04X}) ; {1}".format(value, self.first_operand)
                    elif instructions.is_operand_one_numeric(self.real_operator):
                        self.first_value, error = self.back_patch_label(self.first_operand, np)
                        # self.first_operand = "0x{0:02X}".format(self.first_value)
                    elif instructions.is_operand_one_register(self.real_operator):
                        self.first_value = None

                    if not instructions.is_operand_two_none(self.real_operator):
                        if self.second_operand is not None:
                            if instructions.is_operand_two_numeric(self.real_operator):
                                self.second_value, error = self.back_patch_label(self.second_operand, np)
                                # self.second_operand = "0x{0:02X}".format(self.second_value)
                            elif instructions.is_operand_two_numeric_word(self.real_operator):
                                value, error = self.back_patch_label(self.second_operand, np)
                                if self.good:
                                    self.first_value = value & 0xFF
                                    self.second_value = (value >> 8) & 0xFF
                                    # self.second_operand = "0x{0:04X}".format(value)
                            elif instructions.is_operand_two_memory(self.real_operator):
                                value, error = self.back_patch_label(self.second_operand, np)
                                if self.good:
                                    self.first_value = value & 0xFF
                                    self.second_value = (value >> 8) & 0xFF
                                    # if value != self.second_operand:
                                    #     self.second_operand = "(0x{0:04X}) ; {1}".format(value, self.second_operand)
                                    # else:
                                    #     self.second_operand = "0x{0:04X}".format(value)
                        else:
                            error = "ERROR: Missing second operand"
                            self.good = False
                            self.second_value = None
                            self.second_operand = ''
                else:
                    error = "ERROR: Missing first operand on line {}".format(self.line_number)
                    self.good = False
                    self.first_value = None
                    self.first_operand = ''
        else:
            if self.reserved_space == 0:
                value, error = self.back_patch_label(self.first_operand, np)
                if self.good:
                    self.first_value = value & 0xFF
                    if self.data_size == 2:
                        self.second_value = (value >> 8) & 0xFF
            else:
                self.first_value = int(self.first_operand)

        return error

    def get_memory(self):
        self.memory = [None, None, None]
        if self.good:
            if self.op_code is not None:
                self.memory[0] = self.op_code
                if self.first_value is not None:
                    self.memory[1] = self.first_value
                    if self.second_value is not None:
                        self.memory[2] = self.second_value
                else:
                    if self.second_value is not None:
                        self.memory[1] = self.second_value

            else:
                if self.reserved_space != 0:
                    self.memory = [self.first_value] * self.reserved_space
                else:
                    self.memory[0] = self.first_value
                    if self.second_value is not None:
                        self.memory[1] = self.second_value

        return self.memory

    def get_listing(self):
        listing = "{0:05} - ".format(self.line_number)
        listing += "0x{0:04X}: ".format(self.address)

        memory_dump = ""
        if self.reserved_space != 0:
            memory_dump += "0x00 "
            memory_dump += " ,,, "
            memory_dump += "     "
        else:
            for memory in self.memory:
                if memory is not None:
                    memory_dump += '0x{0:02X} '.format(memory)
                else:
                    memory_dump += "     "

        listing += memory_dump

        if self.label is not None:
            listing += "{:<10s}".format(self.label + ':')
        else:
            listing += "{:<10s}".format(' ')

        if self.operator is None:
            if self.reserved_space != 0:
                listing += " DS {0}".format(self.reserved_space)
            elif self.data_size ==1:
                listing += " DB {0}".format(self.first_operand)
            else:
                listing += " DW {0}".format(self.first_operand)
        else:
            listing += " {}".format(self.operator)
            if self.first_operand is not None:
                listing += " {}".format(self.first_operand)
                if self.second_operand is not None:
                    listing += ", {}".format(self.second_operand)

        listing += "\n"

        return listing
