class Instructions:
    def __init__(self) -> None:
        super().__init__()
        self.operators = {"NOP": {"operator": "NOP", "op_code": 0, "operand": None},
                          "LDA": {"operator": "LDA", "op_code": 1, "operand": "M"},
                          "ADD": {"operator": "ADD", "op_code": 2, "operand": "M"},
                          "SUB": {"operator": "SUB", "op_code": 3, "operand": "M"},
                          "STA": {"operator": "STA", "op_code": 4, "operand": "M"},
                          "LDI": {"operator": "LDI", "op_code": 5, "operand": "N"},
                          "JMP": {"operator": "JMP", "op_code": 6, "operand": "M"},
                          "JC": {"operator": "JC", "op_code": 7, "operand": "M"},
                          "JZ": {"operator": "JZ", "op_code": 8, "operand": "M"},
                          "OUT": {"operator": "OUT", "op_code": 14, "operand": None},
                          "HLT": {"operator": "HLT", "op_code": 15, "operand": None}
                          }

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

    def get_operand_type(self, operator):
        operand_type = None
        if operator in self.operators:
            operand_type = self.operators[operator]["operand"]
        return operand_type

    def is_operand_memory(self, operator):
        return self.get_operand_type(operator) == "M"

    def is_operand_none(self, operator):
        return self.get_operand_type(operator) is None

    def is_operand_numeric(self, operator):
        return self.get_operand_type(operator) == "N"
