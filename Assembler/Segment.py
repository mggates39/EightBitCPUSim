from Cell import Cell

MAX_ADDRSS = 15

class Segment:
    def __init__(self, start, type) -> None:
        super().__init__()
        self.start = start
        self.type = type
        self.address = start
        self.length = 0
        self.label_cell = None
        self.cell_list = []
        self.labels = []

    def getSize(self):
        return self.start + self.length

    def isCode(self):
        return self.type == 'C'

    def overlaps(self, other):
        overlap = False
        if other.start < self.start:
            if other.getSize() > self.start:
                overlap = True
        else:
            if self.getSize() > other.start:
                overlap = True
        return overlap

    def addCell(self, label=None, operator=None, operand=None):
        if self.address <= MAX_ADDRSS:
            if self.label_cell is None:
                cell = Cell(self.address, label, operator, operand)
            else:
                cell = self.label_cell
                cell.operator = operator
                cell.operand = operand
                self.label_cell = None
        else:
            print("ERROR: Maximum segment size exceeded")
            exit(-1)

        self.cell_list.append(cell)
        if cell.label is not None:
            self.labels.append((cell.address, cell.label))
        self.address += 1
        self.length += 1

    def addLabel(self, label):
        self.label_cell = Cell(self.address, label)

    def addInstruction(self, label, operator, operand=None):
        self.addCell(label, operator, operand)

    def addByte(self, label, value):
        self.addCell(label, None, value)

    def assemble(self, labels, instructions):
        for cell in self.cell_list:
            cell.assemble(labels, instructions)

    def loadMemory(self, memory):
        for cell in self.cell_list:
            memory.setMemory(cell.address, cell.getMemory())

        return memory
