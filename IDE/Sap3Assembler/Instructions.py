class Instructions:
    def __init__(self) -> None:
        super().__init__()
        self.mnemonics = {
            "ADD": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ADD A", "ADD B", "ADD C"]},
            "ADI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["ADI"]},
            "ANA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ANA B", "ANA C"]},
            "ANI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["ANI"]},
            "CALL": {"operands": 1, "included": 0, "bytes": 3, "operators": ["CALL"]},
            "CMA": {"operands": 0, "included": 0, "bytes": 1, "operators": ["CMA"]},
            "CMP": {"operands": 1, "included": 1, "bytes": 1, "operators": ["CMP B", "CMP C"]},
            "CPI": {"operands": 1, "included": 0, "bytes": 1, "operators": ["CPI"]},
            "DCR": {"operands": 1, "included": 1, "bytes": 1, "operators": ["DCR A", "DCR B", "DCR C"]},
            "HLT": {"operands": 0, "included": 0, "bytes": 1, "operators": ["HLT"]},
            "IN": {"operands": 1, "included": 0, "bytes": 2, "operators": ["IN"]},
            "INR": {"operands": 1, "included": 1, "bytes": 1, "operators": ["INR A", "INR B", "INR C"]},
            "JC": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JC"]},
            "JM": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JM"]},
            "JMP": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JMP"]},
            "JNC": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JNC"]},
            "JNZ": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JNZ"]},
            "JP": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JP"]},
            "JPE": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JPE"]},
            "JPO": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JPO"]},
            "JZ": {"operands": 1, "included": 0, "bytes": 3, "operators": ["JZ"]},
            "LDA": {"operands": 1, "included": 0, "bytes": 3, "operators": ["LDA"]},
            "LXI": {"operands": 2, "included": 1, "bytes": 3, "operators": ["LXI BC", "LXI DE"]},
            "MOV": {"operands": 2, "included": 2, "bytes": 1,
                    "operators": ["MOV A,A", "MOV A,B", "MOV A,C", "MOV A,D", "MOV A,E", "MOV A,H", "MOV A,L",
                                  "MOV B,A", "MOV B,B", "MOV B,C", "MOV B,D", "MOV B,E", "MOV B,H", "MOV B,L",
                                  "MOV C,A", "MOV C,B", "MOV C,C", "MOV C,D", "MOV C,E", "MOV C,H", "MOV C,L",
                                  "MOV D,A", "MOV D,B", "MOV D,C", "MOV D,D", "MOV D,E", "MOV D,H", "MOV D,L",
                                  "MOV E,A", "MOV E,B", "MOV E,E", "MOV E,D", "MOV E,E", "MOV E,H", "MOV C,L",
                                  "MOV H,A", "MOV H,B", "MOV H,C", "MOV H,D", "MOV H,E", "MOV H,H", "MOV H,L",
                                  "MOV L,A", "MOV L,B", "MOV L,E", "MOV L,D", "MOV L,E", "MOV L,H", "MOV L,L"]},
            "MVI": {"operands": 2, "included": 1, "bytes": 2, "operators": ["MVI A", "MVI B", "MVI C"]},
            "NOP": {"operands": 0, "included": 0, "bytes": 1, "operators": ["NOP"]},
            "ORA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["ORA B", "ORA C"]},
            "ORI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["ORI"]},
            "POP": {"operands": 1, "included": 1, "bytes": 1, "operators": ["POP BC", "POP DE"]},
            "PUSH": {"operands": 1, "included": 1, "bytes": 1, "operators": ["PUSH BC", "PUSH DE"]},
            "OUT": {"operands": 1, "included": 0, "bytes": 2, "operators": ["OUT"]},
            "RAL": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RAL"]},
            "RAR": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RAR"]},
            "RLC": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RLC"]},
            "RRC": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RRC"]},
            "RET": {"operands": 0, "included": 0, "bytes": 1, "operators": ["RET"]},
            "STA": {"operands": 1, "included": 0, "bytes": 3, "operators": ["STA"]},
            "SUB": {"operands": 1, "included": 1, "bytes": 1, "operators": ["SUB A", "SUB B", "SUB C"]},
            "SUI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["SUI"]},
            "XRA": {"operands": 1, "included": 1, "bytes": 1, "operators": ["XRA B", "XRA C"]},
            "XRI": {"operands": 1, "included": 0, "bytes": 2, "operators": ["XRI"]},
        }

        self.operators = {
            "ADD A": {"operator": "ADD A", "op_code": 0x87, "operand1": "A", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ADD B": {"operator": "ADD B", "op_code": 0x80, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ADD C": {"operator": "ADD C", "op_code": 0x81, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "ADI": {"operator": "ADI", "op_code": 0xC6, "operand1": "M", "operand2": None, "addressing": "Imm",
                      "bytes": 2},

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

            "CMP B": {"operator": "CMP B", "op_code": 0xB8, "operand1": "B", "operand2": None, "addressing": "Reg",
                    "bytes": 1},
            "CMP C": {"operator": "CMP C", "op_code": 0xB9, "operand1": "C", "operand2": None, "addressing": "Reg",
                    "bytes": 1},
            "CPI": {"operator": "CPI", "op_code": 0xFE, "operand1": "N", "operand2": None, "addressing": "Imm",
                      "bytes": 2},

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

            "JC": {"operator": "JC", "op_code": 0xDA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JM": {"operator": "JM", "op_code": 0xFA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JMP": {"operator": "JMP", "op_code": 0xC3, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 3},
            "JNC": {"operator": "JNC", "op_code": 0xD2, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 3},
            "JNZ": {"operator": "JNZ", "op_code": 0xC2, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 3},
            "JP": {"operator": "JP", "op_code": 0xF2, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JPE": {"operator": "JPE", "op_code": 0xEA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JPO": {"operator": "JPO", "op_code": 0xE2, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},
            "JZ": {"operator": "JZ", "op_code": 0xCA, "operand1": "M", "operand2": None, "addressing": "Imm",
                   "bytes": 3},

            "LDA": {"operator": "LDA", "op_code": 0x3A, "operand1": "M", "operand2": None, "addressing": "Dir",
                    "bytes": 3},
            "LXI BC": {"operator": "LXI BC", "op_code": 0x01, "operand1": "BC", "operand2": "M", "addressing": "Imm",
                    "bytes": 3},
            "LXI DE": {"operator": "LXI DE", "op_code": 0x11, "operand1": "DE", "operand2": "M", "addressing": "Imm",
                      "bytes": 3},

            "MOV A,A": {"operator": "MOV A,A", "op_code": 0x7F, "operand1": "A", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,B": {"operator": "MOV A,B", "op_code": 0x78, "operand1": "A", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,C": {"operator": "MOV A,C", "op_code": 0x79, "operand1": "A", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,D": {"operator": "MOV A,D", "op_code": 0x7A, "operand1": "A", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,E": {"operator": "MOV A,E", "op_code": 0x7B, "operand1": "A", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,H": {"operator": "MOV A,H", "op_code": 0x7C, "operand1": "A", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV A,L": {"operator": "MOV A,L", "op_code": 0x7D, "operand1": "A", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},

            "MOV B,A": {"operator": "MOV B,A", "op_code": 0x47, "operand1": "B", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,B": {"operator": "MOV B,B", "op_code": 0x40, "operand1": "B", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,C": {"operator": "MOV B,C", "op_code": 0x41, "operand1": "B", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,D": {"operator": "MOV B,D", "op_code": 0x42, "operand1": "B", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,E": {"operator": "MOV B,E", "op_code": 0x43, "operand1": "B", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,H": {"operator": "MOV B,H", "op_code": 0x44, "operand1": "B", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV B,L": {"operator": "MOV B,L", "op_code": 0x45, "operand1": "B", "operand2": "L", "addressing": "Reg",
                        "bytes": 1},

            "MOV C,A": {"operator": "MOV C,A", "op_code": 0x4F, "operand1": "C", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,B": {"operator": "MOV C,B", "op_code": 0x48, "operand1": "C", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,C": {"operator": "MOV C,C", "op_code": 0x49, "operand1": "C", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,D": {"operator": "MOV C,D", "op_code": 0x4A, "operand1": "C", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,E": {"operator": "MOV C,E", "op_code": 0x4B, "operand1": "C", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,H": {"operator": "MOV C,H", "op_code": 0x4C, "operand1": "C", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV C,L": {"operator": "MOV C,L", "op_code": 0x4D, "operand1": "C", "operand2": "L", "addressing": "Reg",
                        "bytes": 1},

            "MOV D,A": {"operator": "MOV D,A", "op_code": 0x57, "operand1": "D", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,B": {"operator": "MOV D,B", "op_code": 0x50, "operand1": "D", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,C": {"operator": "MOV D,C", "op_code": 0x51, "operand1": "D", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,D": {"operator": "MOV D,D", "op_code": 0x52, "operand1": "D", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,E": {"operator": "MOV D,E", "op_code": 0x53, "operand1": "D", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,H": {"operator": "MOV D,H", "op_code": 0x54, "operand1": "D", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV D,L": {"operator": "MOV D,L", "op_code": 0x55, "operand1": "D", "operand2": "L", "addressing": "Reg",
                        "bytes": 1},

            "MOV E,A": {"operator": "MOV E,A", "op_code": 0x5F, "operand1": "E", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,B": {"operator": "MOV E,B", "op_code": 0x58, "operand1": "E", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,C": {"operator": "MOV E,C", "op_code": 0x59, "operand1": "E", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,D": {"operator": "MOV E,D", "op_code": 0x5A, "operand1": "E", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,E": {"operator": "MOV E,E", "op_code": 0x5B, "operand1": "E", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,H": {"operator": "MOV E,H", "op_code": 0x5C, "operand1": "E", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV E,L": {"operator": "MOV E,L", "op_code": 0x5D, "operand1": "E", "operand2": "L", "addressing": "Reg",
                        "bytes": 1},

            "MOV H,A": {"operator": "MOV H,A", "op_code": 0x67, "operand1": "H", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,B": {"operator": "MOV H,B", "op_code": 0x60, "operand1": "H", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,C": {"operator": "MOV H,C", "op_code": 0x61, "operand1": "H", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,D": {"operator": "MOV H,D", "op_code": 0x62, "operand1": "H", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,E": {"operator": "MOV H,E", "op_code": 0x63, "operand1": "H", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,H": {"operator": "MOV H,H", "op_code": 0x64, "operand1": "H", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV H,L": {"operator": "MOV H,L", "op_code": 0x65, "operand1": "H", "operand2": "L", "addressing": "Reg",
                        "bytes": 1},

            "MOV L,A": {"operator": "MOV L,A", "op_code": 0x6F, "operand1": "L", "operand2": "A", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,B": {"operator": "MOV L,B", "op_code": 0x68, "operand1": "L", "operand2": "B", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,C": {"operator": "MOV L,C", "op_code": 0x69, "operand1": "L", "operand2": "C", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,D": {"operator": "MOV L,D", "op_code": 0x6A, "operand1": "L", "operand2": "D", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,E": {"operator": "MOV L,E", "op_code": 0x6B, "operand1": "L", "operand2": "E", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,H": {"operator": "MOV L,H", "op_code": 0x6C, "operand1": "L", "operand2": "H", "addressing": "Reg",
                        "bytes": 1},
            "MOV L,L": {"operator": "MOV L,L", "op_code": 0x6D, "operand1": "L", "operand2": "L", "addressing": "Reg",
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

            "POP BC": {"operator": "POP BC", "op_code": 0xC1, "operand1": "BC", "operand2": None, "addressing": "Reg",
                    "bytes": 2},

            "POP DE": {"operator": "POP DE", "op_code": 0xD1, "operand1": "DE", "operand2": None, "addressing": "Reg",
                    "bytes": 2},

            "PUSH BC": {"operator": "PUSH BC", "op_code": 0xC5, "operand1": "BC", "operand2": None, "addressing": "Reg",
                    "bytes": 2},

            "PUSH DE": {"operator": "PUSH DE", "op_code": 0xD5, "operand1": "DE", "operand2": None, "addressing": "Reg",
                    "bytes": 2},

            "RAL": {"operator": "RAL", "op_code": 0x17, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},
            "RAR": {"operator": "RAR", "op_code": 0x1F, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},
            "RLC": {"operator": "RLC", "op_code": 0x07, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},
            "RDC": {"operator": "RDC", "op_code": 0x0F, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},

            "RET": {"operator": "RET", "op_code": 0xC9, "operand1": None, "operand2": None, "addressing": "Imp",
                    "bytes": 1},

            "STA": {"operator": "STA", "op_code": 0x32, "operand1": "M", "operand2": None, "addressing": "Dir",
                    "bytes": 3},

            "SUB A": {"operator": "SUB A", "op_code": 0x97, "operand1": "A", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "SUB B": {"operator": "SUB B", "op_code": 0x90, "operand1": "B", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "SUB C": {"operator": "SUB C", "op_code": 0x91, "operand1": "C", "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "SUI": {"operator": "SUI", "op_code": 0xD6, "operand1": "M", "operand2": None, "addressing": "Imm",
                    "bytes": 2},

            "XRA B": {"operator": "XRA B", "op_code": 0x90, "operand1": None, "operand2": None, "addressing": "Reg",
                      "bytes": 1},
            "XRA C": {"operator": "XRA C", "op_code": 0x91, "operand1": None, "operand2": None, "addressing": "Reg",
                      "bytes": 1},

            "XRI": {"operator": "XRI", "op_code": 0xEE, "operand1": "N", "operand2": None, "addressing": "Imm",
                    "bytes": 2}
        }

    def is_mnemonic(self, mnemonic):
        return_value = False
        if mnemonic in self.mnemonics:
            return_value = True
        return return_value

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

    def lookup_op_code(self, operator, first_operand, second_operand):
        op_code = -1  # operator not found
        real_operator = None
        if self.is_mnemonic(operator):
            mnemonic = self.get_mnemonic(operator)
            if mnemonic["operands"] == 0:
                op_code = self.operators[operator]["op_code"]
                real_operator = self.get_operator(operator)
            elif mnemonic["operands"] == 1:
                if mnemonic["included"] == 1:
                    test_operator = "{} {}".format(operator, first_operand)
                    if self.is_operator(test_operator):
                        op_code = self.operators[test_operator]["op_code"]
                        real_operator = self.get_operator(test_operator)
                    else:
                        op_code = -2  # Bad Operand
                else:
                    if self.is_operator(operator):
                        op_code = self.operators[operator]["op_code"]
                        real_operator = self.get_operator(operator)

            elif mnemonic["operands"] == 2:
                if mnemonic["included"] == 2:
                    test_operator = "{} {},{}".format(operator, first_operand, second_operand)
                    if self.is_operator(test_operator):
                        op_code = self.operators[test_operator]["op_code"]
                        real_operator = self.get_operator(test_operator)
                    else:
                        op_code = -2  # Bad Operand
                elif mnemonic["included"] == 1:
                    test_operator = "{} {}".format(operator, first_operand)
                    if self.is_operator(test_operator):
                        op_code = self.operators[test_operator]["op_code"]
                        real_operator = self.get_operator(test_operator)
                    else:
                        op_code = -2  # Bad Operand
                else:
                    if self.is_operator(operator):
                        op_code = self.operators[operator]["op_code"]
                        real_operator = self.get_operator(operator)

        return op_code, real_operator

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

    def is_operand_one_register(self, operator):
        return ((self.get_operand_one_type(operator) == "A") |
                (self.get_operand_one_type(operator) == "B") |
                (self.get_operand_one_type(operator) == "C") |
                (self.get_operand_one_type(operator) == "D") |
                (self.get_operand_one_type(operator) == "E") |
                (self.get_operand_one_type(operator) == "H") |
                (self.get_operand_one_type(operator) == "L") |
                (self.get_operand_one_type(operator) == "BC") |
                (self.get_operand_one_type(operator) == "DE"))

    def is_operand_two_memory(self, operator):
        return self.get_operand_two_type(operator) == "M"

    def is_operand_two_none(self, operator):
        return self.get_operand_two_type(operator) is None

    def is_operand_two_numeric(self, operator):
        return self.get_operand_two_type(operator) == "N"

    def is_operand_two_register(self, operator):
        return ((self.get_operand_two_type(operator) == "A") |
                (self.get_operand_two_type(operator) == "B") |
                (self.get_operand_two_type(operator) == "C") |
                (self.get_operand_two_type(operator) == "D") |
                (self.get_operand_two_type(operator) == "E") |
                (self.get_operand_two_type(operator) == "H") |
                (self.get_operand_two_type(operator) == "L") |
                (self.get_operand_two_type(operator) == "BC") |
                (self.get_operand_two_type(operator) == "DE"))
