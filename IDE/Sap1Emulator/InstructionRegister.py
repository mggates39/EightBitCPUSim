import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class InstructionRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Instruction Register", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.HORIZONTAL)

        self.instruction = LEDArray(self.box, 4, topic="ip.set_instruction")
        self.data = LEDArray(self.box, 4, topic="ip.set_data")

        vertical_box.Add(self.instruction, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        vertical_box.Add(self.data, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        self.operators = {0: {"operator": "NOP", "opcode": 0, "operand": None},
                          1: {"operator": "LDA", "opcode": 1, "operand": "M"},
                          2: {"operator": "ADD", "opcode": 2, "operand": "M"},
                          3: {"operator": "SUB", "opcode": 3, "operand": "M"},
                          4: {"operator": "STA", "opcode": 4, "operand": "M"},
                          5: {"operator": "LDI", "opcode": 5, "operand": "N"},
                          6: {"operator": "JMP", "opcode": 6, "operand": "M"},
                          7: {"operator": "JC", "opcode": 7, "operand": "M"},
                          8: {"operator": "JZ", "opcode": 8, "operand": "M"},
                          9: {"operator": "NOP", "opcode": 9, "operand": None},
                          10: {"operator": "NOP", "opcode": 10, "operand": None},
                          11: {"operator": "NOP", "opcode": 11, "operand": None},
                          12: {"operator": "NOP", "opcode": 12, "operand": None},
                          13: {"operator": "NOP", "opcode": 13, "operand": None},
                          14: {"operator": "OUT", "opcode": 14, "operand": None},
                          15: {"operator": "HLT", "opcode": 15, "operand": None}
                          }

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.IrIn')
        pub.subscribe(self.on_out, 'CPU.IrOut')

    def set_in_display_flag(self):
        return True

    def set_out_display_flag(self):
        return True

    def clear_display_flags(self):
        return True

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.on_clock()
        pub.sendMessage('ip.set_instruction', new_value=((self.value >> 4)) & 15)
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage('ip.set_instruction', new_value=((self.value >> 4)) & 15)
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=(self.value & 15))
