import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from Sap1Emulator.MicroCode import MicroCode


class InstructionRegister(wx.Panel):
    def __init__(self, parent, instruction_decoder: MicroCode):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.tick = 0
        self.cycle = 0
        self.ring_count = 0
        self.carry_flag = False
        self.zero_flag = False
        self.instruction_decoder = instruction_decoder
        self.box = wx.StaticBox(self, wx.ID_ANY, "Instruction Register", wx.DefaultPosition, (100, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.read_indicator = wx.StaticText(self.panel, label="IO")
        self.write_indicator = wx.StaticText(self.panel, label="II")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        self.instruction = LEDArray(self.box, 4, topic="ip.set_instruction")
        self.data = LEDArray(self.box, 4, topic="ip.set_data")

        horizontal_box.Add(self.panel, 0, wx.EXPAND)
        horizontal_box.Add(self.instruction, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
        horizontal_box.Add(self.data, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)
        self.operator = None
        self.microcode = []
        self.on_reset()

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.IrIn')
        pub.subscribe(self.on_out, 'CPU.IrOut')
        pub.subscribe(self.on_read_flags, 'alu.FlagValues')
        pub.subscribe(self.on_ring_reset, 'CPU.RingReset')

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()
        microcode = self.microcode[self.ring_count]
        pub.sendMessage("ir.ring", tick=self.tick, cycle=self.cycle, ring=self.ring_count)
        for send in microcode:
            pub.sendMessage(send)
        self.tick += 1
        self.ring_count += 1

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.tick = 0
        self.cycle = 0
        self.ring_count = 0
        self.carry_flag = False
        self.zero_flag = False

        self.clear_display_flags()

        op_code = int((self.value >> 4) & 15)
        self.instruction_decoder.decode_op_code(op_code)
        self.microcode = self.instruction_decoder.get_current_microcode()
        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label="NOP")
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_ring_reset(self):
        self.cycle += 1
        self.ring_count = -1

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        op_code = int((self.value >> 4) & 15)
        self.instruction_decoder.decode_op_code(op_code, carry_flag=self.carry_flag, zero_flag=self.zero_flag)
        operator = self.instruction_decoder.get_current_operator()
        operator_name = operator["operator"]
        self.microcode = self.instruction_decoder.get_current_microcode()

        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label=operator_name)
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=(self.value & 15))

    def on_read_flags(self, new_carry, new_zero):
        self.carry_flag = new_carry
        self.zero_flag = new_zero
