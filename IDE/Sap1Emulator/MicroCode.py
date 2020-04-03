control_messages = [
    {"topic": "CPU.Halt", "label": "HLT"},
    {"topic": "CPU.MarIn", "label": "MI"},
    {"topic": "CPU.MemIn", "label": "RI"},
    {"topic": "CPU.MemOut", "label": "RO"},
    {"topic": "CPU.IrIn", "label": "II"},
    {"topic": "CPU.IrOut", "label": "IO"},
    {"topic": "CPU.ARegIn", "label": "AI"},
    {"topic": "CPU.ARegOut", "label": "AO"},
    {"topic": "CPU.AluOut", "label": "EO"},
    {"topic": "CPU.AluSub", "label": "SU"},
    {"topic": "CPU.TempIn", "label": "TI"},
    {"topic": "CPU.OutputWrite", "label": "OI"},
    {"topic": "CPU.PcOut", "label": "CO"},
    {"topic": "CPU.PcInc", "label": "CE"},
    {"topic": "CPU.PcJump", "label": "CJ"},
    {"topic": "CPU.FlagIn", "label": "FI"},
    {"topic": "CPU.RingReset", "label": "RCR"},
    {"topic": "CPU.IllegalInst", "label": "ILL"}
]

decode_messages = {
    "CPU.Halt": "HLT ",
    "CPU.MarIn": "MI ",
    "CPU.MemIn": "RI ",
    "CPU.MemOut": "RO ",
    "CPU.IrIn": "II ",
    "CPU.IrOut": "IO ",
    "CPU.ARegIn": "AI ",
    "CPU.ARegOut": "AO ",
    "CPU.AluOut": "EO ",
    "CPU.AluSub": "SU ",
    "CPU.TempIn": "TI ",
    "CPU.OutputWrite": "OI ",
    "CPU.PcOut": "CO ",
    "CPU.PcInc": "CE ",
    "CPU.PcJump": "CJ ",
    "CPU.FlagIn": "FI ",
    "CPU.RingReset": "RCR ",
    "CPU.IllegalInst": "ILL "
}

operators = {0: {"operator": "NOP", "op_code": 0, "operand": None,
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.RingReset']]},
             1: {"operator": "LDA <A>", "op_code": 1, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.ARegIn'],
                               ['CPU.RingReset']]},
             2: {"operator": "ADD <A>", "op_code": 2, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.TempIn'],
                               ['CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                               ['CPU.RingReset']]},
             3: {"operator": "SUB <A>", "op_code": 3, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.TempIn'],
                               ['CPU.AluSub', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.ARegIn'],
                               ['CPU.RingReset']]},
             4: {"operator": "STA <A>", "op_code": 4, "operand": "M",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.MarIn'],
                               ['CPU.ARegOut', 'CPU.MemIn'],
                               ['CPU.RingReset']]},
             5: {"operator": "LDI", "op_code": 5, "operand": "N",
                 "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                               ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                               ['CPU.IrOut', 'CPU.ARegIn'],
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
             14: {"operator": "OUT", "op_code": 14, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.ARegOut', 'CPU.OutputWrite'],
                                ['CPU.RingReset']]},
             15: {"operator": "HLT", "op_code": 15, "operand": None,
                  "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                ['CPU.Halt'],
                                ['CPU.RingReset']]}
             }

invalid_operator = {"operator": "***", "op_code": 0, "operand": None,
                    "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                  ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                  ['CPU.IllegalInst', 'CPU.Halt'],
                                  ['CPU.RingReset']]}


class MicroCode:
    def __init__(self):
        self.current_operator = operators[0]
        self.current_microcode = self.current_operator["microcode"]

    def decode_op_code(self, op_code, carry_flag=False, zero_flag=False, negative_flag=False):
        if op_code in operators:
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
        else:
            self.current_operator = invalid_operator
            self.current_microcode = self.current_operator["microcode"]

    def get_current_operator(self):
        return self.current_operator

    def get_current_microcode(self):
        return self.current_microcode
