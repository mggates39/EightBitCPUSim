from Sap1Assembler.Segment import Segment


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
    def __init__(self) -> None:
        super().__init__()
        self.segments = []
        self.active_segment = None

    def get_current_segment(self):
        if self.active_segment is None:
            print("WARNING: No segment has been defined")
            self.active_segment = Segment(0, 'C')
        return self.active_segment

    def start_segment(self, address, segment_type):
        self.end_segment()
        self.active_segment = Segment(address, segment_type)

    def end_segment(self):
        was_active = False
        if self.active_segment is not None:
            self.segments.append(self.active_segment)
            was_active = True
        self.active_segment = None
        return was_active

    def process_directives(self, label, directive, argument=None):
        if argument is None:
            argument = 0
        if directive == '.corg':
            self.start_segment(int(argument), 'C')
        elif directive == '.dorg':
            self.start_segment(int(argument), 'D')
        elif directive == '.end':
            self.end_segment()
        elif directive == '.byte':
            self.get_current_segment().add_byte(label, int(argument))

    def check_for_overlap(self):
        overlap = False
        previous_segment = None

        for segment in self.segments:
            if previous_segment is None:
                previous_segment = segment
            else:
                if previous_segment.overlaps(segment):
                    print("ERROR: Segments overlap: {} segment at {} through {} and {} segment at {} through {}".format(
                        previous_segment.type, previous_segment.start, previous_segment.address,
                        segment.type, segment.start, segment.address, ))
                    overlap = True
                previous_segment = segment

        return overlap

    def parse_fields(self, fields):
        if len(fields) > 0:
            if fields[0].startswith('.'):
                if len(fields) == 2:
                    self.process_directives(None, fields[0], fields[1])
                else:
                    self.process_directives(None, fields[0], None)
            elif fields[0].endswith(':'):
                label = make_label(fields[0])
                if len(fields) == 1:
                    self.get_current_segment().add_label(label)
                elif fields[1].startswith('.'):
                    if len(fields) == 3:
                        self.process_directives(label, fields[1], fields[2])
                    else:
                        self.process_directives(label, fields[1], None)
                elif len(fields) == 3:
                    self.get_current_segment().add_instruction(label, fields[1], make_target(fields[2]))
                else:
                    self.get_current_segment().add_instruction(label, fields[1], None)
            else:
                if len(fields) == 2:
                    self.get_current_segment().add_instruction(None, fields[0], make_target(fields[1]))
                else:
                    self.get_current_segment().add_instruction(None, fields[0], None)

    def parse_strings(self, lines):
        for line in lines:
            # Ignore comment lines
            if line.startswith('#') or line.startswith(';'):
                continue

            fields = line.split()
            self.parse_fields(fields)

        if self.end_segment():
            print("WARNING: Source file does not have .end directive.")

        if self.check_for_overlap():
            exit(-1)

        return self.segments

    def parse_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()

        return self.parse_strings(lines)
