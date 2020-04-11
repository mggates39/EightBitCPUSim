from Sap3Assembler.Cell import Cell

MAX_ADDRESS = 4096


class Segment:
    def __init__(self, start, segment_type, instructions) -> None:
        super().__init__()
        self.start = start
        self.type = segment_type
        self.instructions = instructions
        self.address = start
        self.length = 0
        self.label_cell = None
        self.cell_list = []
        self.labels = []
        self.errors = []

    def get_last_address(self):
        return self.start + self.length

    def is_code(self):
        return self.type == 'C'

    def overlaps(self, other):
        overlap = False
        if other.start < self.start:
            if other.get_last_address() > self.start:
                overlap = True
        else:
            if self.get_last_address() > other.start:
                overlap = True
        return overlap

    def define_label(self, label, value):
        self.labels.append((value, label))

    def add_cell(self, line_number, label=None, operator=None, first_operand=None, second_operand=None, data_size=0, reserved_space=0, data_array=None):
        if self.address <= MAX_ADDRESS:
            if self.label_cell is None:
                cell = Cell(line_number, self.address, label, operator, first_operand, second_operand, data_size, reserved_space, data_array)
            else:
                cell = self.label_cell
                cell.line_number = line_number
                cell.operator = operator
                cell.first_operand = first_operand
                cell.second_operand = second_operand
                cell.data_size = data_size
                cell.reserved_space = reserved_space
                cell.data_array = data_array
                self.label_cell = None
            cell.calculate_size(self.instructions)

            self.cell_list.append(cell)
            if cell.label is not None:
                self.labels.append((cell.address, cell.label))
            self.address += cell.get_size()
            self.length += cell.get_size()

        else:
            self.errors.append("ERROR: Segment will not fit in memory at address 0x{0:04X}!\n".format(self.address))

    def add_label(self, line_number, label):
        if self.address <= MAX_ADDRESS:
            self.label_cell = Cell(line_number, self.address, label)
        else:
            self.errors.append("ERROR: Segment will not fit in memory at address 0x{0:04X}!\n".format(self.address))

    def add_instruction(self, line_number, label, operator, first_operand=None, second_operand=None):
        self.add_cell(line_number, label, operator, first_operand, second_operand)

    def reserve_space(self, line_number, label, number_bytes):
        self.add_cell(line_number, label, None, 0, None, 0, number_bytes)

    def add_byte(self, line_number, label, operand):
        self.add_cell(line_number, label, None, operand, None, 1)

    def add_word(self, line_number, label, operand):
        self.add_cell(line_number, label, None, operand, None, 2)

    def add_array(self, line_number, label, operand, data_size, data_array):
        self.add_cell(line_number, label, None, operand, None, -data_size, 0, data_array)

    def assemble(self, np):
        error = "ERROR: Segment with no operands or directives at address 0x{0:04X}\n".format(self.address)
        for cell in self.cell_list:
            error = cell.assemble_pass_one(self.instructions)
            if error != "":
                self.errors.append(error)
                error = ""

        if error == "":
            for cell in self.cell_list:
                error = cell.assemble_pass_two(self.instructions, np)
                if error != "":
                    self.errors.append(error)
        else:
            self.errors.append(error)

    def load_memory(self, memory):
        for cell in self.cell_list:
            memory.set_memory(cell.address, cell.get_memory())

        return memory

    def get_listing(self):
        listing = "\n\tORG 0x{0:04X}\n".format(self.start)
        for cell in self.cell_list:
            listing += cell.get_listing()

        return listing

    def get_errors(self):
        return self.errors
