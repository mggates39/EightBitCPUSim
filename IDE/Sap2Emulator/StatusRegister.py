import wx
from pubsub import pub

from GuiComponents.Led import LED


class StatusRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.carry = False
        self.zero = False
        self.minus = False
        light_color = '#36ff27'
        dark_color = '#077100'
        self.box = wx.StaticBox(self, wx.ID_ANY, "Status Register", wx.DefaultPosition, (100, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        carry_box = wx.BoxSizer(wx.HORIZONTAL)
        self.carry_flag = wx.StaticText(self.box, label="Carry:", style=wx.ALIGN_RIGHT)
        self.carry_led = LED(self.box, light_color, dark_color)
        carry_box.Add(self.carry_flag, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        carry_box.Add(self.carry_led, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        zero_box = wx.BoxSizer(wx.HORIZONTAL)
        self.zero_flag = wx.StaticText(self.box, label="Zero:", style=wx.ALIGN_RIGHT)
        self.zero_led = LED(self.box, light_color, dark_color)
        zero_box.Add(self.zero_flag, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        zero_box.Add(self.zero_led, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        negative_box = wx.BoxSizer(wx.HORIZONTAL)
        self.minus_flag = wx.StaticText(self.box, label="Minus:", style=wx.ALIGN_RIGHT)
        self.minus_led = LED(self.box, light_color, dark_color)
        negative_box.Add(self.minus_flag, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        negative_box.Add(self.minus_led, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        vertical_box.Add(carry_box, 1, wx.EXPAND | wx.ALIGN_CENTER)
        vertical_box.Add(zero_box, 1, wx.EXPAND | wx.ALIGN_CENTER)
        vertical_box.Add(negative_box, 1, wx.EXPAND | wx.ALIGN_CENTER)
        horizontal_box.Add(vertical_box, 1, wx.EXPAND | wx.ALIGN_CENTER)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.write_indicator = wx.StaticText(self.panel, label="FI")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)
        horizontal_box.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.set_in_display_flag, "CPU.FlagIn")
        pub.subscribe(self.on_get_flags, "alu.FlagValues")

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.carry = False
        self.zero = False
        self.minus = False
        self.clear_display_flags()
        self.display_flags()

    def on_get_flags(self, new_carry, new_zero, new_minus):
        self.set_in_display_flag()
        self.carry = new_carry
        self.zero = new_zero
        self.minus = new_minus
        self.display_flags()

    def display_flags(self):
        self.carry_led.light(self.carry)
        self.zero_led.light(self.zero)
        self.minus_led.light(self.minus)
