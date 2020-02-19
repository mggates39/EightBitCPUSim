import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class Alu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.result = 0
        self.a_value = 0
        self.b_value = 0
        self.carry = False
        self.zero = False
        self.subtract = False
        self.box = wx.StaticBox(self, wx.ID_ANY, "ALU", wx.DefaultPosition, (100, 75))
        self.nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=( 30, 75))
        self.read_indicator = wx.StaticText(self.panel, label="EO")
        self.subtract_indicator = wx.StaticText(self.panel, label="SU")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.subtract_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="alu.set_value")
        self.carry_flag =  wx.StaticText(self.box, label="Carry-Bit: False", style=wx.ALIGN_CENTRE)
        self.zero_flag =  wx.StaticText(self.box, label="Zero-Bit: False", style=wx.ALIGN_CENTRE)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
        vertical_box.Add(self.carry_flag, 0, wx.ALIGN_CENTER | wx.ALL,10)
        vertical_box.Add(self.zero_flag, 0, wx.ALIGN_CENTER | wx.ALL,10)

        hbox.Add(vertical_box, 1, wx.EXPAND)
        hbox.Add(self.panel, 0, wx.EXPAND)

        self.nmSizer.Add(hbox, 1, wx.EXPAND)

        self.SetSizer(self.nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_a_value, 'alu.set_value_1')
        pub.subscribe(self.on_b_value, 'alu.set_value_2')
        pub.subscribe(self.on_out, 'CPU.AluOut')
        pub.subscribe(self.on_subtract, 'CPU.AluSub')
        pub.subscribe(self.on_save_flags, 'CPU.FlagIn')


    def set_sub_display_flag(self):
        self.subtract_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.subtract_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.subtract = False
        self.clear_display_flags()
        self.do_math()

    def on_reset(self):
        self.result = 0
        self.a_value = 0
        self.b_value = 0
        self.carry = False
        self.zero = False
        self.subtract = False
        self.on_clock()

    def on_a_value(self, new_value):
        self.a_value = new_value
        self.do_math()

    def on_b_value(self, new_value):
        self.b_value = new_value
        self.do_math()

    def on_subtract(self):
        self.set_sub_display_flag()
        self.subtract = True
        self.do_math()

    def do_math(self):
        if self.subtract:
            self.result = self.a_value - self.b_value
            if self.a_value != 0:
                self.carry = True
            else:
                self.carry = False
        else:
            self.result = self.a_value + self.b_value
            if self.result >= 255:
                self.result = self.result & 255
                self.carry = True
            else:
                self.carry = False
        if self.result == 0:
            self.zero = True
        else:
            self.zero = False

        self.set_carry_lablel(self.carry)
        self.set_zero_lablel(self.zero)
        pub.sendMessage('alu.set_value', new_value=self.result)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.result)

    def on_save_flags(self):
        pub.sendMessage("alu.FlagValues", new_carry=self.carry, new_zero=self.zero)

    def set_carry_lablel(self, new_label: bool) -> None:
        """
        Set the value to be displayed by the Carry Flag.
        :type new_value: str
        :rtype: None
        """
        self.carry_flag.SetLabel("Carry-Bit: {}".format(new_label))
        self.nmSizer.Layout()

    def set_zero_lablel(self, new_label: bool) -> None:
        """
        Set the value to be displayed by the Carry Flag.
        :type new_value: str
        :rtype: None
        """
        self.zero_flag.SetLabel("Zero-Bit: {}".format(new_label))
        self.nmSizer.Layout()
