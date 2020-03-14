import unittest
from Sap3Assembler.Instructions import Instructions
from Sap3Emulator.MicroCode import MicroCode
from Sap3Emulator.MicroCode import operators

class MyTestCase(unittest.TestCase):
    def test_all_parsable_are_define(self):

        instructions = Instructions()
        result = True

        for mnemonic in instructions.mnemonics:
            mnemonic_details = instructions.get_mnemonic(mnemonic)
            for operator in mnemonic_details["operators"]:
                details = instructions.get_operator(operator)
                if details is None:
                    print("Warning: mnemonic {} is not an operator.".format(operator))
                    result = False


        self.assertEqual(True, result)

    def test_all_parsable_are_implemented(self):

        instructions = Instructions()
        microcode = MicroCode()
        result = True

        for operator in instructions.operators:
            details = instructions.get_operator(operator)
            microcode.decode_op_code(details["op_code"])
            lookup = microcode.get_current_operator()
            if lookup["operator"] != details["operator"]:
                print("Warning: operator {0} - 0x{1:02X} is not implemented.".format(details["operator"], details["op_code"]))
                result = False

        self.assertEqual(True, result)

    def test_all_implemented_are_parsable(self):

        instructions = Instructions()
        microcode = MicroCode()
        result = True

        for op_code in operators:
            micro_details = operators[op_code]
            details = instructions.get_operator(micro_details["operator"])

            if details is None:
                print("Warning: operator {0} - 0x{1:02X} is not parseable.".format(micro_details["operator"], micro_details["op_code"]))
                result = False

        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
