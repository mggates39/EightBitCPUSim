from Cell import Cell


class origin:
    def __init__(self, start, type) -> None:
        super().__init__()
        self.start = start
        self.type = type
        self.address = start
        self.length = 0
        self.currentCell = None
        self.cellList = []
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

    def addLabel(self, label):
        self.currentCell = Cell(self.address, label)

    def addInstruction(self, label, op_code, argument=None):
        if self.currentCell == None:
            cell = Cell(self.address, label, op_code, argument)
        else:
            cell = self.currentCell
            cell.opcode = op_code
            cell.value = argument
            self.currentCell = None

        self.cellList.append(cell)
        if cell.label != None:
            self.labels.append((cell.address, cell.label))
        self.address += 1
        self.length += 1

    def addByte(self, label, value):
        if self.currentCell == None:
            cell = Cell(self.address, label, None, value)
            cell.value = value
        else:
            cell = self.currentCell
            cell.value = value
            self.currentCell = None

        self.cellList.append(cell)
        if cell.label != None:
            self.labels.append((cell.address, cell.label))
        self.address += 1
        self.length += 1

    def loadMemory(self, memory):
        for cell in self.cellList:
            memory.setMemory(cell.address, cell.getMemory())

        return memory
