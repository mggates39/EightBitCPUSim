import math

from pyparsing import ParseException

from Sap3Assembler.NumericStringParser import NumericStringParser

if __name__ == "__main__":
    good = {"STACK" : 15, "TEMP0": 512}

    np = NumericStringParser()
    np.set_labels(good)


    def test(s, expVal):
        global np
        try:
            val = np.eval(s)
        except ParseException as pe:
            print(s, "failed parse:", str(pe))
        except Exception as e:
            print(s, "failed eval:", str(e))
        else:
            if val == expVal:
                print(s, "=", val)
            else:
                print(s + "!!!", val, "!=", expVal)


    test("9", 9)
    test("-9", -9)
    test("--9", 9)
    test("-E", -math.e)
    test("9 + 3 + 6", 9 + 3 + 6)
    test("9 + 3 / 11", 9 + 3.0 / 11)
    test("(9 + 3)", (9 + 3))
    test("(9+3) / 11", (9 + 3.0) / 11)
    test("9 - 12 - 6", 9 - 12 - 6)
    test("9 - (12 - 6)", 9 - (12 - 6))
    test("2*3.14159", 2 * 3.14159)
    test("3.1415926535*3.1415926535 / 10", 3.1415926535 * 3.1415926535 / 10)
    test("PI * PI / 10", math.pi * math.pi / 10)
    test("PI*PI/10", math.pi * math.pi / 10)
    test("PI^2", math.pi ** 2)
    test("round(PI^2)", round(math.pi ** 2))
    test("6.02E23 * 8.048", 6.02E23 * 8.048)
    test("e / 3", math.e / 3)
    test("sin(PI/2)", math.sin(math.pi / 2))
    test("trunc(E)", int(math.e))
    test("trunc(-E)", int(-math.e))
    test("round(E)", round(math.e))
    test("round(-E)", round(-math.e))
    test("E^PI", math.e ** math.pi)
    test("2^3^2", 2 ** 3 ** 2)
    test("2^3+2", 2 ** 3 + 2)
    test("2^3+5", 2 ** 3 + 5)
    test("2^9", 2 ** 9)
    test("sgn(-2)", -1)
    test("sgn(0)", 0)
    test("foo(0.1)", 1)
    test("sgn(0.1)", 1)
    test("5 & 3", 1)
    test("4 | 3", 7)
    test("STACK", 3)
    test("TEMP0", 512)
    test("int(TEMP0/0FFH)", 2)
    test("harry", "harry")
    test("0FFH", 255)
    test("0xFF", 255)
