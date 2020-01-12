from Segment import Segment

class Parser:
    def __init__(self) -> None:
        super().__init__()
        self.segments = []
        self.active_segement = None

    def make_target(self, target):
        fixed_target = target[:-1]
        fixed_target = fixed_target[1:]
        return fixed_target

    def make_label(self, label):
        fixed_label = label[:-1]
        return fixed_label

    def get_current_segment(self):
        if self.active_segement is None:
            print("WARNING: No segemnt has been defined")
            self.active_segement = Segment(0,'C')
        return self.active_segement

    def start_segment(self, address, type):
        self.end_segment()
        self.active_segement = Segment(address, type)

    def end_segment(self):
        was_active = False
        if self.active_segement is not None:
            self.segments.append(self.active_segement)
            was_active = True
        self.active_segement = None
        return was_active

    def process_directives(self, label, directive, argument=None):
        if directive == '.corg':
            self.start_segment(int(argument), 'C')
        elif directive == '.dorg':
            self.start_segment(int(argument), 'D')
        elif directive == '.end':
            self.end_segment()
        elif directive == '.byte':
            self.get_current_segment().add_byte(label, int(argument))

    def parse_file(self, file_name):
        f = open(file_name, "r")
        fl = f.readlines()
        for x in fl:
            # Ignore comment lines
            if x.startswith('#'):
                continue

            fields = x.split()

            if len(fields) > 0:
                if fields[0].startswith('.'):
                    if len(fields) == 2:
                        self.process_directives(None, fields[0], fields[1])
                    else:
                        self.process_directives(None, fields[0], None)
                elif fields[0].endswith(':'):
                    label = self.make_label(fields[0])
                    if len(fields) == 1:
                        self.get_current_segment().add_label(label)
                    elif fields[1].startswith('.'):
                        self.process_directives(label, fields[1], fields[2])
                    elif len(fields) == 3:
                        self.get_current_segment().add_instruction(label, fields[1], self.make_target(fields[2]))
                    else:
                        self.get_current_segment().add_instruction(label, fields[1], None)
                else:
                    if len(fields) == 2:
                        self.get_current_segment().add_instruction(None, fields[0], self.make_target(fields[1]))
                    else:
                        self.get_current_segment().add_instruction(None, fields[0], None)

        if self.end_segment():
            print("WARNING: Segment not properly ended")

        previousSegment = None
        for segment in self.segments:
            if previousSegment is None:
                previousSegment = segment
            else:
                if previousSegment.overlaps(segment):
                    print("ERROR: Segments overlap")
                    exit(-1)
                previousSegment = segment

        return self.segments
