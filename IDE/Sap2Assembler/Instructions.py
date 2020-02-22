class Instructions:
    def __init__(self) -> None:
        super().__init__()
        self.mnemonics = {
            "ADD": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ADD B", "ADD C"]},
            "ANA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ANA B", "ANA C"]},
            "ANI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["ANI"]},
            "CALL": {"operands": 1, "included": 0, "bytes": 3, "operators": ["CALL"]},
            "CMA": {"operands": 0, "included": 0, "bytes": 1, "operators": ["CMA"]},
            "DCR": {"operands": 1, "included": 1, "bytes": 1, "operators": ["DCR A", "DCR B", "DCR C"]},
            "HLT": {"operands": 0, "included": 0, "bytes": 1, "operators": ["HLT"]},
            "IN": {"operands": 1, "included": 0, "bytes": 2, "operators": ["IN"]},
            "INR": {"operands": 1, "included": 1, "bytes": 1, "operators": ["INR A", "INR B", "INR C"]},
            "JC": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JC"]},
            "JM": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JM"]},
            "JMP": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JMP"]},
            "JNZ": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JNZ"]},
            "JZ": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JZ"]},
            "LDA": {"operands": 1, "included": 0, "bytes": 3, "operators": ["LDA"]},
            "MOV": {"operands": 2, "included": 21, "bytes": 1,
                    "operators": ["MOV A,B", "MOV A,C", "MOV B,A", "MOV B,C", "MOV C,A", "MOV C,B"]},
            "MVI": {"operands": 2, "included": 0, "bytes": 2, "operators": ["MVI A", "MVI B", "MVI C"]},
            "NOP": {"operands": 0, "included": 0, "bytes": 1, "operators": ["NOP"]},
            "ORA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ORA B", "ORA C"]},
            "ORI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["ORI"]},
            "OUT": {"operands": 1, "included": 0, "bytes": 2, "operators": ["OUT"]},
            "RAL": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RAL"]},
            "RAR": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RAR"]},
            "RET": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RET"]},
            "STA": {"operands": 1, "included": 0, "bytes": 3, "operators": ["STA"]},
            "SUB": {"operands": 1, "included": 1, "bytes": 1, "operators": ["SUB B", "SUB C"]},
            "XRA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["XRA B", "XRA C"]},
            "XRI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["XRI"]},
        }

        self.operators = {
            "ADD B": {"operator": "ADD B", "op_code": 0x80, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ADD C": {"operator": "ADD C", "op_code": 0x81, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "ANA B": {"operator": "ANA B", "op_code": 0xA0, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ANA C": {"operator": "ANA C", "op_code": 0xA1, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "ANI": {"operator": "ANI", "op_code": 0xE6, "operand1": "N", "operand2": None, "addressing": "Imm",
                    "bytes": 2},

            "CALL": {"operator": "CALL", "op_code": 0xCD, "operand1": "M", "operand2": None, "addressing": "Imm",
                     "bytes": 3},

            "CMA": {"operator": "CMA", "op_code": 0x2F, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},

            "DCR A": {"operator": "DCR A", "op_code": 0x3D, "operand1": "A", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "DCR B": {"operator": "DCR B", "op_code": 0x05, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "DCR C": {"operator": "DCR C", "op_code": 0x0D, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "HLT": {"operator": "HLT", "op_code": 0x76, "operand1": None, "operand2": None, "addressing": "Non",
                    "bytes": 1},

            "IN": {"operator": "IN", "op_code": 0xDB, "operand1": "N", "operand2": None, "addressing": "Dir",
                   "bytes": 2},

            "INR A": {"operator": "INR A", "op_code": 0x3C, "operand1": "A", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "INR B": {"operator": "INR B", "op_code": 0x04, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "INR C": {"operator": "INR C", "op_code": 0x0C, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "JC": {"operator": "JC", "op_code": 0xFB, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JM": {"operator": "JM", "op_code": 0xFA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JMP": {"operator": "JMP", "op_code": 0xC3, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 3},
            "JNZ": {"operator": "JNZ", "op_code": 0xC2, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 3},
            "JZ": {"operator": "JZ", "op_code": 0xCA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},

            "LDA": {"operator": "LDA", "op_code": 0x3A, "operand1": "M", "operand2": None, "addressing": "Dir",
                    "bytes": 3},

            "MOV A,B": {"operator": "MOV A,B", "op_code": 0x78, "operand1": "A", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,C": {"operator": "MOV A,C", "op_code": 0x79, "operand1": "A", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},

            "MOV B,A": {"operator": "MOV B,A", "op_code": 0x47, "operand1": "B", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,C": {"operator": "MOV B,C", "op_code": 0x41, "operand1": "B", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},

            "MOV C,A": {"operator": "MOV C,A", "op_code": 0x4F, "operand1": "C", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,B": {"operator": "MOV C,B", "op_code": 0x48, "operand1": "C", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},

            "MVI A": {"operator": "MVI A", "op_code": 0x3E, "operand1": "A", "operand2": "N", "addressing": "Imm",
                      "bytes": 2},
            "MVI B": {"operator": "MVI B", "op_code": 0x06, "operand1": "B", "operand2": "N", "addressing": "Imm",
                      "bytes": 2},
            "MVI C": {"operator": "MVI C", "op_code": 0x0E, "operand1": "C", "operand2": "N", "addressing": "Imm",
                      "bytes": 2},

            "NOP": {"operator": "NOP", "op_code": 0x00, "operand1": None, "operand2": None, "addressing": "Non",
                    "bytes": 1},

            "ORA B": {"operator": "ORA B", "op_code": 0xB0, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ORA C": {"operator": "ORA C", "op_code": 0xB1, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "ORI": {"operator": "ORI", "op_code": 0xF6, "operand1": "N", "operand2": None, "addressing": "Imm",
                    "bytes": 2},

            "OUT": {"operator": "OUT", "op_code": 0xD3, "operand1": "N", "operand2": None, "addressing": "Dir",
                    "bytes": 2},

            "RAL": {"operator": "RAL", "op_code": 0x17, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},
            "RAR": {"operator": "RAR", "op_code": 0x1F, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},

            "RET": {"operator": "RET", "op_code": 0xC9, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},

            "STA": {"operator": "STA", "op_code": 0x32, "operand1": "M", "operand2": None, "addressing": "Dir",
                    "bytes": 3},

            "SUB B": {"operator": "SUB B", "op_code": 0x90, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "SUB C": {"operator": "SUB C", "op_code": 0x91, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "XRA B": {"operator": "XRA B", "op_code": 0x90, "operand1": None, "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "XRA C": {"operator": "XRA C", "op_code": 0x91, "operand1": None, "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "XRI": {"operator": "XRI", "op_code": 0xEE, "operand1": "N", "operand2": None, "addressing": "Imm",
                    "bytes": 2}
        }

    def get_mnemonic(self, mnemonic):
        if mnemonic in self.mnemonics:
            return self.mnemonics[mnemonic]
        else:
            return None

    def get_operator(self, operator):
        if operator in self.operators:
            return self.operators[operator]
        else:
            return None

    def is_operator(self, operator):
        return_value = False
        if operator in self.operators:
            return_value = True
        return return_value

    def lookup_op_code(self, operator):
        op_code = -1
        if self.is_operator(operator):
            op_code = self.operators[operator]["op_code"]
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
