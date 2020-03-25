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

    def process_directives(self, line_number, label, directive, argument=None):
        if argument is None:
            argument = 0
        else:
            if argument[-1] == 'H':
                argument = int(argument[:-1], 16)
        if directive == '.org':
            self.start_segment(int(argument), 'C')
        elif directive == '.corg':
            self.start_segment(int(argument), 'C')
        elif directive == '.dorg':
            self.start_segment(int(argument), 'D')
        elif directive == '.end':
            self.end_segment()
        elif directive == '.byte':
            self.get_current_segment().add_byte(line_number, label, int(argument))
        elif directive == '.word':
            self.get_current_segment().add_word(line_number, label, int(argument))

    def check_for_overlap(self):
        overlap = False
        previous_segment = None

        for segment in self.segments:
            if previous_segment is None:
                previous_segment = segment
            else:
                if previous_segment.overlaps(segment):
                    overlap = True
                    self.errors.append(
                        "ERROR: Segments overlap: Segment at 0x{0:04X} through 0x{1:04X} and segment at 0x{2:04X} through 0x{3:04X}!\n".format(
                            previous_segment.start, previous_segment.address, segment.start, segment.address))
                previous_segment = segment

        return overlap

    def process_instructions(self, line_number, label, fields):
        if label is not None:
            if len(fields) == 2:
                self.get_current_segment().add_instruction(line_number, label, fields[1], None)
            else:
                arguments = fields[2].split(',')
                if len(arguments) == 1:
                    self.get_current_segment().add_instruction(line_number, label, fields[1], make_target(fields[2]))
                else:
                    self.get_current_segment().add_instruction(line_number, label, fields[1], make_target(arguments[0]),
                                                               make_target(arguments[1]))

        else:
            if len(fields) == 2:
                arguments = fields[1].split(',')
                if len(arguments) == 1:
                    self.get_current_segment().add_instruction(line_number, None, fields[0], make_target(fields[1]))
                else:
                    self.get_current_segment().add_instruction(line_number, None, fields[0], make_target(arguments[0]),
                                                               make_target(arguments[1]))
            else:
                self.get_current_segment().add_instruction(line_number, None, fields[0], None)

    def parse_fields(self, line_number, fields):
        if len(fields) > 0:
            if fields[0].startswith('.'):
                if len(fields) == 2:
                    self.process_directives(line_number, None, fields[0], fields[1])
                else:
                    self.process_directives(line_number, None, fields[0], None)
            elif fields[0].endswith(':'):
                label = make_label(fields[0])
                if len(fields) == 1:
                    self.get_current_segment().add_label(line_number, label)
                elif fields[1].startswith('.'):
                    if len(fields) == 3:
                        self.process_directives(line_number, label, fields[1], fields[2])
                    else:
                        self.process_directives(line_number, label, fields[1], None)
                else:
                    self.process_instructions(line_number, label, fields)
            else:
                self.process_instructions(line_number, None, fields)

    def parse_strings(self, lines):
        line_number = 0
        for line in lines:
            line_number += 1
            # Ignore comment lines
            if line.startswith('#') or line.startswith(';'):
                continue

            rest = line.split(';',1)[0]

            fields = rest.split()
            self.parse_fields(line_number, fields)

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
