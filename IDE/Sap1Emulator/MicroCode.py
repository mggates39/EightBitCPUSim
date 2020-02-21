control_messages = {
    0: {"topic": "CPU.Halt", "label": "HLT"},
    1: {"topic": "CPU.MarIn", "label": "MI"},
    2: {"topic": "CPU.MemIn", "label": "RI"},
    3: {"topic": "CPU.MemOut", "label": "RO"},
    4: {"topic": "CPU.IrIn", "label": "II"},
    5: {"topic": "CPU.IrOut", "label": "IO"},
    6: {"topic": "CPU.AccIn", "label": "AI"},
    7: {"topic": "CPU.AccOut", "label": "AO"},

    8: {"topic": "CPU.AluOut", "label": "EO"},
    9: {"topic": "CPU.AluSub", "label": "SU"},
    10: {"topic": "CPU.TempIn", "label": "BI"},
    11: {"topic": "CPU.OutputWrite", "label": "OI"},

    12: {"topic": "CPU.PcOut", "label": "CO"},
    13: {"topic": "CPU.PcInc", "label": "CE"},
    14: {"topic": "CPU.PcJump", "label": "CJ"},
    15: {"topic": "CPU.FlagIn", "label": "FI"},
    16: {"topic": "CPU.RingReset", "label": "RCR"},
}

decode_messages = {
    "CPU.Halt": "HLT ",
    "CPU.MarIn": "MI ",
    "CPU.MemIn": "RI ",
    "CPU.MemOut": "RO ",
    "CPU.IrIn": "II ",
    "CPU.IrOut": "IO ",
    "CPU.AccIn": "AI ",
    "CPU.AccOut": "AO ",
    "CPU.AluOut": "EO ",
    "CPU.AluSub": "SU ",
    "CPU.TempIn": "BI ",
    "CPU.OutputWrite": "OI ",
    "CPU.PcOut": "CO ",
    "CPU.PcInc": "CE ",
    "CPU.PcJump": "CJ ",
    "CPU.FlagIn": "FI ",
    "CPU.RingReset": "RCR "
}

operators = {0: {"operator": "NOP", "op_code": 0, "operand": None,
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.RingReset']]},
             1: {"operator": "LDA <A>", "op_code": 1, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.AccIn'],
                               ['CPU.RingReset']]},
             2: {"operator": "ADD <A>", "op_code": 2, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.TempIn'],
                               ['CPU.FlagIn', 'CPU.AluOut', 'CPU.AccIn'],
                               ['CPU.RingReset']]},
             3: {"operator": "SUB <A>", "op_code": 3, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.TempIn'],
                               ['CPU.AluSub', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.AccIn'],
                               ['CPU.RingReset']]},
             4: {"operator": "STA <A>", "op_code": 4, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.AccOut', 'CPU.MemIn'],
                               ['CPU.RingReset']]},
             5: {"operator": "LDI", "op_code": 5, "operand": "N",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.AccIn'],
                               ['CPU.RingReset']]},
             6: {"operator": "JMP <A>", "op_code": 6, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.PcJump'],
                               ['CPU.RingReset']]},
             7: {"operator": "JC <A>", "op_code": 7, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.RingReset']]},
             8: {"operator": "JZ <A>", "op_code": 8, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.RingReset']]},
             9: {"operator": "JNZ <A>", "op_code": 9, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.RingReset']]},
             10: {"operator": "JM <A>", "op_code": 10, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.RingReset']]},
             11: {"operator": "NOP", "op_code": 11, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.RingReset']]},
             12: {"operator": "NOP", "op_code": 12, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.RingReset']]},
             13: {"operator": "NOP", "op_code": 13, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.RingReset']]},
             14: {"operator": "OUT", "op_code": 14, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.AccOut', 'CPU.OutputWrite'],
                                ['CPU.RingReset']]},
             15: {"operator": "HLT", "op_code": 15, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.Halt'],
                                ['CPU.RingReset']]}
             }


class MicroCode:
    def __init__(self):
        self.current_operator = operators[0]
        self.current_microcode = self.current_operator["microcode"]

    def decode_op_code(self, op_code, carry_flag=False, zero_flag=False, negative_flag=False):
        self.current_operator = operators[op_code]
        self.current_microcode = self.current_operator["microcode"]

        if op_code == 7 and carry_flag:
            self.current_microcode = operators[6]["microcode"]

        if op_code == 8 and zero_flag:
            self.current_microcode = operators[6]["microcode"]

        if op_code == 9 and zero_flag:
            self.current_microcode = operators[6]["microcode"]

        if op_code == 10 and negative_flag:
            self.current_microcode = operators[6]["microcode"]

    def get_current_operator(self):
        return self.current_operator

    def get_current_microcode(self):
        return self.current_microcode
