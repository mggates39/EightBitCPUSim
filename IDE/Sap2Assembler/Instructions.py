class Instructions:
    def __init__(self) -> None:
        super().__init__()
        self.operators = {"ADD B": {"operator": "ADD B", "opcode": 0x80, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "ADD C": {"operator": "ADD C", "opcode": 0x81, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "ANA B": {"operator": "ANA B", "opcode": 0xA0, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "ANA C": {"operator": "ANA C", "opcode": 0xA1, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "ANI": {"operator": "ANI", "opcode": 0xE6, "operand1": "N", "operand2": None,
                                  "addressing": "Imm", "bytes": 2},

                          "CALL": {"operator": "CALL", "opcode": 0xCD, "operand1": "M", "operand2": None,
                                   "addressing": "Imm", "bytes": 3},

                          "CMA": {"operator": "CMA", "opcode": 0x2F, "operand1": None, "operand2": None,
                                  "addressing": "Imp", "bytes": 1},

                          "DCR A": {"operator": "DCR A", "opcode": 0x3D, "operand1": "A", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "DCR B": {"operator": "DCR B", "opcode": 0x05, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "DCR C": {"operator": "DCR C", "opcode": 0x0D, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "HLT": {"operator": "HLT", "opcode": 0x76, "operand1": None, "operand2": None,
                                  "addressing": "Non", "bytes": 1},

                          "IN": {"operator": "IN", "opcode": 0xDB, "operand1": "N", "operand2": None,
                                 "addressing": "Dir", "bytes": 2},

                          "INR A": {"operator": "INR A", "opcode": 0x3C, "operand1": "A", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "INR B": {"operator": "INR B", "opcode": 0x04, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "INR C": {"operator": "INR C", "opcode": 0x0C, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "JM": {"operator": "JM", "opcode": 0xFA, "operand1": "M", "operand2": None,
                                 "addressing": "Imm", "bytes": 3},
                          "JMP": {"operator": "JMP", "opcode": 0xC3, "operand1": "M", "operand2": None,
                                  "addressing": "Imm", "bytes": 3},
                          "JNZ": {"operator": "JNZ", "opcode": 0xC2, "operand1": "M", "operand2": None,
                                  "addressing": "Imm", "bytes": 3},
                          "JZ": {"operator": "JZ", "opcode": 0xCA, "operand1": "M", "operand2": None,
                                 "addressing": "Imm", "bytes": 3},

                          "LDA": {"operator": "LDA", "opcode": 0x3A, "operand1": "N", "operand2": None,
                                  "addressing": "Dir", "bytes": 3},

                          "MOV A,B": {"operator": "MOV A,B", "opcode": 0x78, "operand1": "A", "operand2": "B",
                                      "addressing": "Reg", "bytes": 1},
                          "MOV A,C": {"operator": "MOV A,C", "opcode": 0x79, "operand1": "A", "operand2": "C",
                                      "addressing": "Reg", "bytes": 1},

                          "MOV B,A": {"operator": "MOV B,A", "opcode": 0x47, "operand1": "B", "operand2": "A",
                                      "addressing": "Reg", "bytes": 1},
                          "MOV B,C": {"operator": "MOV B,C", "opcode": 0x41, "operand1": "B", "operand2": "C",
                                      "addressing": "Reg", "bytes": 1},

                          "MOV C,A": {"operator": "MOV C,A", "opcode": 0x4F, "operand1": "C", "operand2": "A",
                                      "addressing": "Reg", "bytes": 1},
                          "MOV C,B": {"operator": "MOV C,B", "opcode": 0x48, "operand1": "C", "operand2": "B",
                                      "addressing": "Reg", "bytes": 1},

                          "MVI A": {"operator": "MVI A", "opcode": 0x3E, "operand1": "A", "operand2": "N",
                                    "addressing": "Imm", "bytes": 2},
                          "MVI B": {"operator": "MVI B", "opcode": 0x06, "operand1": "B", "operand2": "N",
                                    "addressing": "Imm", "bytes": 2},
                          "MVI C": {"operator": "MVI C", "opcode": 0x0E, "operand1": "C", "operand2": "N",
                                    "addressing": "Imm", "bytes": 2},

                          "NOP": {"operator": "NOP", "opcode": 0x00, "operand1": None, "operand2": None,
                                  "addressing": "Non", "bytes": 1},

                          "ORA B": {"operator": "ORA B", "opcode": 0xB0, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "ORA C": {"operator": "ORA C", "opcode": 0xB1, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "ORI": {"operator": "ORI", "opcode": 0xF6, "operand1": "N", "operand2": None,
                                  "addressing": "Imm", "bytes": 2},

                          "OUT": {"operator": "OUT", "opcode": 0xD3, "operand1": "N", "operand2": None,
                                  "addressing": "Dir", "bytes": 2},

                          "RAL": {"operator": "RAL", "opcode": 0x17, "operand1": None, "operand2": None,
                                  "addressing": "Imp", "bytes": 1},
                          "RAR": {"operator": "RAR", "opcode": 0x1F, "operand1": None, "operand2": None,
                                  "addressing": "Imp", "bytes": 1},

                          "RET": {"operator": "RET", "opcode": 0xC9, "operand1": None, "operand2": None,
                                  "addressing": "Imp", "bytes": 1},

                          "STA": {"operator": "STA", "opcode": 0x32, "operand1": "M", "operand2": None,
                                  "addressing": "Dir", "bytes": 3},

                          "SUB B": {"operator": "SUB B", "opcode": 0x90, "operand1": "B", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "SUB C": {"operator": "SUB C", "opcode": 0x91, "operand1": "C", "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "XRA B": {"operator": "XRA B", "opcode": 0x90, "operand1": None, "operand2": None,
                                    "addressing": "Reg", "bytes": 1},
                          "XRA C": {"operator": "XRA C", "opcode": 0x91, "operand1": None, "operand2": None,
                                    "addressing": "Reg", "bytes": 1},

                          "XRI": {"operator": "XRI", "opcode": 0xEE, "operand1": "N", "operand2": None,
                                  "addressing": "Imm", "bytes": 2}
                          }

    def is_operator(self, operator):
        return_value = False
        if operator in self.operators:
            return_value = True
        return return_value

    def lookup_op_code(self, operator):
        op_code = 0
        if self.is_operator(operator):
            op_code = self.operators[operator]["opcode"]
        return op_code

    def get_operand_one_type(self, operator):
        operand_type = None
        if operator in self.operators:
            operand_type = self.operators[operator]["operand1"]
        return operand_type

    def get_operand_two_type(self, operator):
        operand_type = None
        if operator in self.operators:
            operand_type = self.operators[operator]["operand2"]
        return operand_type

    def is_operand_one_memory(self, operator):
        return self.get_operand_one_type(operator) == "M"

    def is_operand_one_none(self, operator):
        return self.get_operand_one_type(operator) is None

    def is_operand_one_numeric(self, operator):
        return self.get_operand_one_type(operator) == "N"

    def is_operand_two_memory(self, operator):
        return self.get_operand_two_type(operator) == "M"

    def is_operand_two_none(self, operator):
        return self.get_operand_two_type(operator) is None

    def is_operand_two_numeric(self, operator):
        return self.get_operand_two_type(operator) == "N"
