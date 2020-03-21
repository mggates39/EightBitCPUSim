import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedArray import MODE_HEX
from Sap3Emulator.MicroCode import MicroCode


class InstructionRegister(wx.Panel):
    def __init__(self, parent, instruction_decoder: MicroCode):
        wx.Panel.__init__(self, parent, size=(100, 150))
        self.parent = parent
        self.value = 0
        self.operand = 0
        self.buffer = 0
        self.tick = 0
        self.cycle = 0
        self.ring_count = 0
        self.active = False
        self.carry_flag = False
        self.zero_flag = False
        self.sign_flag = False
        self.parity_flag = False
        self.auxillary_carry_flag = False
        self.instruction_decoder = instruction_decoder
        self.box = wx.StaticBox(self, wx.ID_ANY, "Instruction Register", wx.DefaultPosition, (100, 150))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(40, 75))
        self.read_indicator = wx.StaticText(self.panel, label="IO")
        self.write_indicator = wx.StaticText(self.panel, label="II")
        self.load_operand_low_indicator = wx.StaticText(self.panel, label="IAL")
        self.load_operand_high_indicator = wx.StaticText(self.panel, label="IAH")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.load_operand_low_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.load_operand_high_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        self.instruction = LEDArray(self.box, 8, topic="ip.set_instruction")
        self.data = LEDArray(self.box, 16, topic="ip.set_data", size=10, mode=MODE_HEX)
        register_box = wx.BoxSizer(wx.VERTICAL)
        register_box.Add(self.instruction, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        register_box.Add(self.data, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        horizontal_box.Add(self.panel, 0, wx.EXPAND)
        horizontal_box.Add(register_box, 1, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)
        self.operator = None
        self.microcode = []
        self.on_reset()

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.IrIn')
        pub.subscribe(self.on_operand_low, 'CPU.IrAlIn')
        pub.subscribe(self.on_operand_high, 'CPU.IrAhIn')
        pub.subscribe(self.on_out, 'CPU.IrOut')
        pub.subscribe(self.on_read_flags, 'alu.FlagValues')
        pub.subscribe(self.on_ring_reset, 'CPU.RingReset')
        pub.subscribe(self.on_active, 'clock.active')

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_load_low_display_flag(self):
        self.load_operand_low_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_load_high_display_flag(self):
        self.load_operand_high_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.load_operand_low_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.load_operand_high_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_active(self,new_active):
        self.active = new_active

    def on_clock(self):
        self.clear_display_flags()
        if self.active:
            microcode = self.microcode[self.ring_count]
            pub.sendMessage("ir.ring", tick=self.tick, cycle=self.cycle, ring=self.ring_count)
            for send in microcode:
                pub.sendMessage(send)
            self.tick += 1
            self.ring_count += 1

    def on_reset(self):
        self.value = 0
        self.operand = 0
        self.buffer = 0
        self.tick = 0
        self.cycle = 0
        self.ring_count = 0
        self.active = False
        self.carry_flag = False
        self.zero_flag = False
        self.sign_flag = False
        self.parity_flag = False
        self.auxillary_carry_flag = False

        self.clear_display_flags()

        op_code = self.value
        self.instruction_decoder.decode_op_code(op_code)
        self.microcode = self.instruction_decoder.get_current_microcode()
        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label="NOP")
        pub.sendMessage('ip.set_data', new_value=self.operand)

    def on_ring_reset(self):
        self.cycle += 1
        self.ring_count = -1

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.operand = 0
        self.set_in_display_flag()
        op_code = int(self.value)
        self.instruction_decoder.decode_op_code(op_code, carry_flag=self.carry_flag, zero_flag=self.zero_flag,
                                                sign_flag=self.sign_flag, parity_flag=self.parity_flag,
                                                auxillary_carry_flag=self.auxillary_carry_flag)
        operator = self.instruction_decoder.get_current_operator()
        operator_name = operator["operator"]
        self.microcode = self.instruction_decoder.get_current_microcode()

        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label=operator_name)
        pub.sendMessage('ip.set_data', new_value=self.operand)

    def on_operand_low(self):
        self.operand = int(self.buffer)
        self.set_load_low_display_flag()
        pub.sendMessage('ip.set_data', new_value=self.operand)

    def on_operand_high(self):
        self.operand = (int(self.buffer) << 8) + self.operand
        self.set_load_high_display_flag()
        pub.sendMessage('ip.set_data', new_value=self.operand)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.operand)

    def on_read_flags(self, new_carry, new_zero, new_sign, new_parity, new_auxillary_carry):
        self.auxillary_carry_flag = new_auxillary_carry
        self.carry_flag = new_carry
        self.zero_flag = new_zero
        self.sign_flag = new_sign
        self.parity_flag = new_parity
