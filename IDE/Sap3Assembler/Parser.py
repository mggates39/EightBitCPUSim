import re

from Sap3Assembler.Instructions import Instructions
from Sap3Assembler.Segment import Segment


def make_label(label):
    fixed_label = label[:-1]
    return fixed_label


def is_label(target):
    label_found = False
    if target.startswith('<') or target.startswith('('):
        label_found = True
    return label_found


def make_target(target):
    fixed_target = target
    if is_label(fixed_target):
        fixed_target = fixed_target[:-1]
        fixed_target = fixed_target[1:]
    return fixed_target


class Parser:
    def __init__(self, instructions: Instructions) -> None:
        super().__init__()
        self.instructions = instructions
        self.segments = []
        self.errors = []
        self.active_segment = None

    def get_current_segment(self):
        if self.active_segment is None:
            self.errors.append("WARNING: No segment has been defined!\n")
            self.active_segment = Segment(0, 'C', self.instructions)
        return self.active_segment

    def start_segment(self, address, segment_type):
        self.end_segment()
        self.active_segment = Segment(address, segment_type, self.instructions)

    def end_segment(self):
        was_active = False
        if self.active_segment is not None:
            self.segments.append(self.active_segment)
            was_active = True
        self.active_segment = None
        return was_active

    def add_symbol(self, label, value):
        if self.active_segment is not None:
            self.active_segment.define_label(label, value)

    def process_directives(self, line_number, label, directive, argument=None):
        if argument is None:
            argument = 0
        else:
            if argument[-1] == 'H':
                argument = int(argument[:-1], 16)
            elif argument[0:1] == '0X':
                argument = int(argument[2:], 16)
        real_directive = self.instructions.get_directive(directive)["directive"]
        if real_directive == "ORG":
            self.start_segment(int(argument), 'C')
        elif real_directive == '.corg':
            self.start_segment(int(argument), 'C')
        elif real_directive == '.dorg':
            self.start_segment(int(argument), 'D')
        elif real_directive == 'END':
            self.end_segment()
        elif real_directive == 'DB':
            self.get_current_segment().add_byte(line_number, label, argument)
        elif real_directive == 'DW':
            self.get_current_segment().add_word(line_number, label, argument)
        elif real_directive == 'DS':
            self.get_current_segment().reserve_space(line_number, label, int(argument))
        elif real_directive == 'EQU':
            self.add_symbol(label, argument)


    def check_for_overlap(self):
        overlap = False

        for segment1 in self.segments:
            for segment2 in self.segments:
                if segment1 != segment2:
                    if segment1.overlaps(segment2):
                        overlap = True
                        self.errors.append(
                            "ERROR: Segments overlap: Segment at 0x{0:04X} through 0x{1:04X} and segment at 0x{2:04X} through 0x{3:04X}!\n".format(
                                segment1.start, segment1.address, segment2.start, segment2.address))

        return overlap

    def process_instructions(self, line_number, label, operator, operand_one, opearnd_two):
        if operand_one is not None:
            operand_one = make_target(operand_one.rstrip())
        if opearnd_two is not None:
            opearnd_two = make_target(opearnd_two.rstrip())
        operator = operator.rstrip()

        self.get_current_segment().add_instruction(line_number, label, operator, operand_one, opearnd_two)

    def parse_fields(self, line_number, fields):
        my_fields = [None, None, None, None]
        label = None
        if fields[0] is not None:
            label = make_label(fields[0])

        if len(fields) == 1:
            self.get_current_segment().add_label(line_number, label)
        else:
            i = 0
            for field in fields:
                my_fields[i] = field
                i += 1

            if self.instructions.is_directive(my_fields[1]):
                self.process_directives(line_number, label, my_fields[1], my_fields[2])
            elif self.instructions.is_mnemonic(my_fields[1]):
                self.process_instructions(line_number, label, my_fields[1], my_fields[2], my_fields[3])
            else:
                self.errors.append("ERROR: Unknown operator or directive {0} at line {1}.\n".format(my_fields[1], line_number))

    def parse_strings(self, lines):
        line_number = 0
        b = re.compile(r'^\s*$')
        p = re.compile(r'^(.*:)?\s(.*)\s(.*),\s?(.*)')
        s = re.compile(r'^(.*:)?\s(.*)\s(.*)')
        t = re.compile(r'^(.*:)?\s(.*)')
        q = re.compile(r'^(.*:)')
        for line in lines:
            line_number += 1
            # Ignore comment lines and comments at the end of lines
            if line.startswith('#') or line.startswith(';'):
                continue

            rest = (line.split(';', 1)[0]).rstrip()

            m = b.match(rest)
            if not m:
                m = p.match(rest)
                if not m:
                    m = s.match(rest)
                    if not m:
                        m = t.match(rest)
                        if not m:
                            m = q.match(rest)

                if m:
                    self.parse_fields(line_number, m.groups())

        if self.end_segment():
            self.errors.append("WARNING: Source file does not have .end directive.\n")

        self.check_for_overlap()

        return self.segments

    def parse_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()

        return self.parse_strings(lines)

    def get_errors(self):
        return self.errors
