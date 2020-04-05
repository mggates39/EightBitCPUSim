from __future__ import division
import pyparsing as pyp
import math
import operator


class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example
    http://pyparsing.wikispaces.com/file/view/fourFn.py
    http://pyparsing.wikispaces.com/message/view/home/15549426
    __author__='Paul McGuire'

    All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
    more easily in other places.
    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self, labels=[]):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-' | '&'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        self.labels = labels
        point = pyp.Literal(".")
        e = pyp.CaselessLiteral("E")
        # fnumber = pyp.Combine(pyp.Word("+-" + pyp.nums, pyp.nums) +
        #                       pyp.Optional(point + pyp.Optional(pyp.Word(pyp.nums))) +
        #                       pyp.Optional(e + pyp.Word("+-" + pyp.nums, pyp.nums)))
        fnumber = pyp.Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?")
        hexnumber = pyp.Regex(R"(0x([0-9a-fA-F]+)|([0-9a-fA-F]+)H)")
        ident = pyp.Word(pyp.alphas, pyp.alphas + pyp.nums + "_$")
        label = pyp.Word(pyp.alphas, pyp.alphas + pyp.nums)
        plus = pyp.Literal("+")
        minus = pyp.Literal("-")
        mult = pyp.Literal("*")
        div = pyp.Literal("/")
        and_ = pyp.Literal("&")
        or_ = pyp.Literal("|")
        land = pyp.Literal("AND")
        lor = pyp.Literal("OR")
        lxor = pyp.Literal("XOR")
        lpar = pyp.Literal("(").suppress()
        rpar = pyp.Literal(")").suppress()
        addop = plus | minus | and_ | or_ | land | lor | lxor
        multop = mult | div
        expop = pyp.Literal("^")
        pi = pyp.CaselessLiteral("PI")
        expr = pyp.Forward()
        atom = ((pyp.Optional(pyp.oneOf("- +")) +
                 (pi | e | hexnumber | fnumber | ident + lpar + expr + rpar).setParseAction(self.pushFirst))
                | (label).setParseAction(self.pushFirst)
                | pyp.Optional(pyp.oneOf("- +")) + pyp.Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = pyp.Forward()
        factor << atom + pyp.ZeroOrMore((expop + factor).setParseAction(
            self.pushFirst))
        term = factor + pyp.ZeroOrMore((multop + factor).setParseAction(
            self.pushFirst))
        expr << term + pyp.ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow,
                    "&": operator.and_,
                    "AND": operator.and_,
                    "|": operator.or_,
                    "OR": operator.or_,
                    "XOR": operator.xor}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "int": int,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   # For Python3 compatibility, cmp replaced by ((a > 0) - (a < 0)). See
                   # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
                   "sgn": lambda a: abs(a) > epsilon and ((a > 0) - (a < 0)) or 0}
        self.exprStack = []

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        if op in ["&","|","AND","OR","XOR"]:
            op2 = int(self.evaluateStack(s))
            op1 = int(self.evaluateStack(s))
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            if op in self.labels:
                return self.labels[op]
            else:
                return op
        elif op[:2] == '0x':
            return int(op[2:], 16)
        elif op[-1:] == 'H':
            return int(op[:-1], 16)
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val

    def set_labels(self, labels):
        self.labels = labels