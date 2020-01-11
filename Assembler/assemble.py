from Memory import Memory
from Instructions import Instructions
from origin import origin

def loadCodeFile():
    fileOrigins = []
    codeOrigin = origin(0,'C')
    codeOrigin.addInstruction("top", "LDA", "x")
    codeOrigin.addInstruction(None, "SUB", "One")
    codeOrigin.addInstruction(None, "JC", "continue")
    codeOrigin.addInstruction(None, "LDA", "product")
    codeOrigin.addInstruction(None, "OUT")
    codeOrigin.addInstruction(None, "HLT")
    codeOrigin.addInstruction("continue", "STA", "x")
    codeOrigin.addInstruction(None, "LDA", "product")
    codeOrigin.addInstruction(None, "ADD", "y")
    codeOrigin.addInstruction(None, "STA", "product")
    codeOrigin.addInstruction(None, "JMP", "top")
    fileOrigins.append(codeOrigin)

    dataOrigin = origin(12, 'D')
    dataOrigin.addByte("One", 1)
    dataOrigin.addByte("product", 0)
    dataOrigin.addByte("x", 3)
    dataOrigin.addByte("y", 29)
    fileOrigins.append(dataOrigin)

    return fileOrigins

labels = []
origins = []
m = Memory()
i = Instructions()

origins = loadCodeFile()

for origin in origins:
    for label in origin.labels:
        labels.append(label)

for origin in origins:
    if origin.isCode():
        for cell in origin.cellList:
            cell.assemble(labels, i)

for origin in origins:
    if origin.isCode():
        codeOrigin = origin
    m = origin.loadMemory(m)

m.dump(labels, codeOrigin.cellList)

