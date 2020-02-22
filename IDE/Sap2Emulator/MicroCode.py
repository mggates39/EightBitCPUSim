control_messages = [
    {"topic": "CPU.Halt", "label": "HLT"},

    {"topic": "CPU.MarIn", "label": "MI"},
    {"topic": "CPU.MemIn", "label": "RI"},
    {"topic": "CPU.MemOut", "label": "RO"},

    {"topic": "CPU.IrIn", "label": "II"},
    {"topic": "CPU.IrAlIn", "label": "IAL"},
    {"topic": "CPU.IrAhIn", "label": "IAH"},
    {"topic": "CPU.IrOut", "label": "IO"},

    {"topic": "CPU.ARegIn", "label": "AI"},
    {"topic": "CPU.ARegOut", "label": "AO"},
    {"topic": "CPU.BRegIn", "label": "BI"},
    {"topic": "CPU.BRegOut", "label": "BO"},
    {"topic": "CPU.CRegIn", "label": "CI"},
    {"topic": "CPU.CRegOut", "label": "CO"},

    {"topic": "CPU.AluAdd", "label": "ADD"},
    {"topic": "CPU.AluCma", "label": "CMA"},
    {"topic": "CPU.AluDec", "label": "DEC"},
    {"topic": "CPU.AluInc", "label": "INC"},
    {"topic": "CPU.AluLand", "label": "LAND"},
    {"topic": "CPU.AluLda", "label": "LDA"},
    {"topic": "CPU.AluLdb", "label": "LDB"},
    {"topic": "CPU.AluLdc", "label": "LDC"},
    {"topic": "CPU.AluLor", "label": "LOR"},
    {"topic": "CPU.AluLxor", "label": "LXOR"},
    {"topic": "CPU.AluOut", "label": "EO"},
    {"topic": "CPU.AluRar", "label": "RAR"},
    {"topic": "CPU.AluRal", "label": "RAL"},
    {"topic": "CPU.AluSub", "label": "SUB"},

    {"topic": "CPU.TempIn", "label": "TI"},

    {"topic": "CPU.OutputWrite", "label": "OI"},

    {"topic": "CPU.PcOut", "label": "CO"},
    {"topic": "CPU.PcInc", "label": "CE"},
    {"topic": "CPU.PcJump", "label": "CJ"},
    {"topic": "CPU.FlagIn", "label": "FI"},

    {"topic": "CPU.RingReset", "label": "RCR"}
]

decode_messages = {
    "CPU.Halt": "HLT ",
    "CPU.MarIn": "MI ",
    "CPU.MemIn": "RI ",
    "CPU.MemOut": "RO ",
    "CPU.IrIn": "II ",
    "CPU.IrAlIn": "IAL ",
    "CPU.IrAhIn": "IAH ",
    "CPU.IrOut": "IO ",
    "CPU.ARegIn": "AI ",
    "CPU.ARegOut": "AO ",
    "CPU.BRegIn": "BI ",
    "CPU.BRegOut": "BO ",
    "CPU.CRegIn": "CI ",
    "CPU.CRegOut": "CO ",
    "CPU.AluLda": "LDA ",
    "CPU.AluLdb": "LDB ",
    "CPU.AluLdc": "LDC ",
    "CPU.AluLand": "LAND ",
    "CPU.AluLor": "LOR ",
    "CPU.AluLxor": "LXOR ",
    "CPU.AluOut": "EO ",
    "CPU.AluAdd": "ADD ",
    "CPU.AluSub": "SUB ",
    "CPU.AluDec": "DEC ",
    "CPU.AluInc": "INC ",
    "CPU.AluRar": "RAR ",
    "CPU.AluRal": "RAL ",
    "CPU.AluCma": "CMA ",
    "CPU.TempIn": "TI ",
    "CPU.OutputWrite": "OI ",
    "CPU.PcOut": "CO ",
    "CPU.PcInc": "CE ",
    "CPU.PcJump": "CJ ",
    "CPU.FlagIn": "FI ",
    "CPU.RingReset": "RCR "
}

operators = {
    0x00: {"operator": "NOP", "op_code": 0x00, "operand1": None, "operand2": None, "addressing": "Non",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.RingReset']]},

    0xD3: {"operator": "OUT", "op_code": 0xD3, "operand1": "N", "operand2": None, "addressing": "Dir",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         # Need output port selection from operand
                         ['CPU.RingReset']]},

    0x04: {"operator": "INR B", "op_code": 0x04, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLdb', 'CPU.AluInc', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.BRegIn'],
                         ['CPU.RingReset']]},
    0x05: {"operator": "DCR B", "op_code": 0x05, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLdb', 'CPU.AluInc', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.BRegIn'],
                         ['CPU.RingReset']]},
    0x06: {"operator": "MVI B", "op_code": 0x06, "operand1": "B", "operand2": "N", "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.BRegIn'],
                         ['CPU.RingReset']]},

    0x0C: {"operator": "INR C", "op_code": 0x0C, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLdc', 'CPU.AluInc', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.CRegIn'],
                         ['CPU.RingReset']]},
    0x0D: {"operator": "DCR C", "op_code": 0x0D, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLdc', 'CPU.AluDec', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.CRegIn'],
                         ['CPU.RingReset']]},
    0x0E: {"operator": "MVI C", "op_code": 0x0E, "operand1": "C", "operand2": "N", "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.CRegIn'],
                         ['CPU.RingReset']]},

    0x17: {"operator": "RAL", "op_code": 0x17, "operand1": None, "operand2": None, "addressing": "Imp",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLda', 'CPU.AluRal', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x1F: {"operator": "RAR", "op_code": 0x1F, "operand1": None, "operand2": None, "addressing": "Imp",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLda', 'CPU.AluRar', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x2F: {"operator": "CMA", "op_code": 0x2F, "operand1": None, "operand2": None, "addressing": "Imp",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLda', 'CPU.AluCma', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x32: {"operator": "STA", "op_code": 0x32, "operand1": "M", "operand2": None, "addressing": "Dir",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.MarIn'],
                         ['CPU.ARegOut', 'CPU.MemIn'],
                         ['CPU.RingReset']]},

    0x3A: {"operator": "LDA", "op_code": 0x3A, "operand1": "M", "operand2": None, "addressing": "Dir",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x3C: {"operator": "INR A", "op_code": 0x3C, "operand1": "A", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLda', 'CPU.AluInc', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x3D: {"operator": "DCR A", "op_code": 0x3D, "operand1": "A", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.AluLda', 'CPU.AluInc', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x3E: {"operator": "MVI A", "op_code": 0x3E, "operand1": "A", "operand2": "N", "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x41: {"operator": "MOV B,C", "op_code": 0x41, "operand1": "B", "operand2": "C", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.BRegIn'],
                         ['CPU.RingReset']]},
    0x47: {"operator": "MOV B,A", "op_code": 0x47, "operand1": "B", "operand2": "A", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.ARegOut', 'CPU.BRegIn'],
                         ['CPU.RingReset']]},

    0x48: {"operator": "MOV C,B", "op_code": 0x48, "operand1": "C", "operand2": "B", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BARegOut', 'CPU.CRegIn'],
                         ['CPU.RingReset']]},
    0x4F: {"operator": "MOV C,A", "op_code": 0x4F, "operand1": "C", "operand2": "A", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.ARegOut', 'CPU.CRegIn'],
                         ['CPU.RingReset']]},

    0x76: {"operator": "HLT", "op_code": 0x76, "operand1": None, "operand2": None, "addressing": "Non",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.Halt'],
                         ['CPU.RingReset']]},

    0x78: {"operator": "MOV A,B", "op_code": 0x78, "operand1": "A", "operand2": "B", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x79: {"operator": "MOV A,C", "op_code": 0x79, "operand1": "A", "operand2": "C", "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x80: {"operator": "ADD B", "op_code": 0x80, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluAdd', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x81: {"operator": "ADD C", "op_code": 0x81, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluAdd', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0x90: {"operator": "SUB B", "op_code": 0x90, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluSub', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0x91: {"operator": "SUB C", "op_code": 0x91, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluSub', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0xA0: {"operator": "ANA B", "op_code": 0xA0, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLand', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0xA1: {"operator": "ANA C", "op_code": 0xA1, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLand', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0xA8: {"operator": "XRA B", "op_code": 0xA8, "operand1": None, "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLxor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0xA9: {"operator": "XRA C", "op_code": 0xA9, "operand1": None, "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLxor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0xB0: {"operator": "ORA B", "op_code": 0xB0, "operand1": "B", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.BRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0xB1: {"operator": "ORA C", "op_code": 0xB1, "operand1": "C", "operand2": None, "addressing": "Reg",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.CRegOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0xC2: {"operator": "JNZ", "op_code": 0xC2, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.RingReset']]},
    0xC3: {"operator": "JMP", "op_code": 0xC3, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.PcJump'],
                         ['CPU.RingReset']]},
    0xC9: {"operator": "RET", "op_code": 0xC9, "operand1": None, "operand2": None, "addressing": "Imp",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         # Meed get return address into PC
                         ['CPU.RingReset']]},
    0xCA: {"operator": "JZ", "op_code": 0xCA, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.RingReset']]},
    0xCD: {"operator": "CALL", "op_code": 0xCD, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         # Need Save return address from PC
                         ['CPU.RingReset']]},

    0xDB: {"operator": "IN", "op_code": 0xDB, "operand1": "N", "operand2": None, "addressing": "Dir",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         # Need input port select
                         ['CPU.RingReset']]},

    0xE6: {"operator": "ANI", "op_code": 0xE6, "operand1": "N", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLand', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0xEE: {"operator": "XRI", "op_code": 0xEE, "operand1": "N", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.TempIn'],
                         ['CPU.AluLda', 'CPU.AluLxor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},
    0xF6: {"operator": "ORI", "op_code": 0xF6, "operand1": "N", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.IrOut', 'CPU.TempIn'],
                         'CPU.AluLda', ['CPU.AluLor', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                         ['CPU.RingReset']]},

    0xFA: {"operator": "JM", "op_code": 0xFA, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.RingReset']]},
    0xFB: {"operator": "JC", "op_code": 0xFB, "operand1": "M", "operand2": None, "addressing": "Imm",
           "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAlIn', 'CPU.PcInc'],
                         ['CPU.PcOut', 'CPU.MarIn'],
                         ['CPU.MemOut', 'CPU.IrAhIn', 'CPU.PcInc'],
                         ['CPU.RingReset']]},
}

invalid_operator = {"operator": "***", "op_code": 0x00, "operand1": None, "operand2": None, "addressing": "Non",
                    "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                  ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                  ['CPU.Halt'],
                                  ['CPU.RingReset']]}


class MicroCode:
    def __init__(self):
        self.current_operator = operators[0]
        self.current_microcode = self.current_operator["microcode"]

    def decode_op_code(self, op_code, carry_flag=False, zero_flag=False, negative_flag=False):
        if op_code in operators:
            self.current_operator = operators[op_code]
            self.current_microcode = self.current_operator["microcode"]

            # JC
            if op_code == 0xFB and carry_flag:
                self.current_microcode = operators[0xC3]["microcode"]

            # JNZ
            if op_code == 0xC2 and not zero_flag:
                self.current_microcode = operators[0xC3]["microcode"]

            # JZ
            if op_code == 0xCA and zero_flag:
                self.current_microcode = operators[0xC3]["microcode"]

            # JM
            if op_code == 0xFA and negative_flag:
                self.current_microcode = operators[0xC3]["microcode"]
        else:
            self.current_operator = invalid_operator
            self.current_microcode = self.current_operator["microcode"]

    def get_current_operator(self):
        return self.current_operator

    def get_current_microcode(self):
        return self.current_microcode
