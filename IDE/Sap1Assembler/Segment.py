from Sap1Assembler.Cell import Cell

MAX_ADDRESS = 15


class Segment:
    def __init__(self, start, segment_type) -> None:
        super().__init__()
        self.start = start
        self.type = segment_type
        self.address = start
        self.length = 0
        self.label_cell = None
        self.cell_list = []
        self.labels = []
        self.errors = []

    def get_size(self):
        return self.start + self.length

    def is_code(self):
        return self.type == 'C'

    def overlaps(self, other):
        overlap = False
        if other.start < self.start:
            if other.get_size() > self.start:
                overlap = True
        else:
            if self.get_size() > other.start:
                overlap = True
        return overlap

    def add_cell(self, label=None, operator=None, operand=None):
        if self.address <= MAX_ADDRESS:
            if self.label_cell is None:
                cell = Cell(self.address, label, operator, operand)
            else:
                cell = self.label_cell
                cell.operator = operator
                cell.operand = operand
                self.label_cell = None

            self.cell_list.append(cell)
            if cell.label is not None:
                self.labels.append((cell.address, cell.label))
            self.address += 1
            self.length += 1

        else:
            self.errors.append("ERROR: Segment will not fit in memory at address {}!\n".format(self.address))

    def add_label(self, label):
        if self.address <= MAX_ADDRESS:
            self.label_cell = Cell(self.address, label)
        else:
            self.errors.append("ERROR: Segment will not fit in memory at address {}!\n".format(self.address))

    def add_instruction(self, label, operator, operand=None):
        self.add_cell(label, operator, operand)

    def add_byte(self, label, value):
        self.add_cell(label, None, value)

    def assemble(self, labels, instructions):
        for cell in self.cell_list:
            error = cell.assemble(labels, instructions)
            if error != "":
                self.errors.append(error)

    def load_memory(self, memory):
        for cell in self.cell_list:
            memory.set_memory(cell.address, cell.get_memory())

        return memory

    def get_listing(self):
        listing = "\n\t.org {}\n".format(self.start)
        for cell in self.cell_list:
            listing += cell.get_listing()

        return listing

    def get_errors(self):
        return self.errors
