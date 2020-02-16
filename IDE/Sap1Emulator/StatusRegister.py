import wx
from pubsub import pub

from GuiComponents.Led import LED


class StatusRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.carry = False
        self.zero = False
        light_color = '#36ff27'
        dark_color = '#077100'
        self.box = wx.StaticBox(self, wx.ID_ANY, "Status Register", wx.DefaultPosition, (100,75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        carry_box = wx.BoxSizer(wx.HORIZONTAL)
        self.carry_flag =  wx.StaticText(self.box, label="Carry:", style=wx.ALIGN_RIGHT)
        self.carry_led = LED(self.box, light_color, dark_color)
        carry_box.Add(self.carry_flag,0, wx.ALL|wx.ALIGN_RIGHT, 5)
        carry_box.Add(self.carry_led,0, wx.ALL|wx.ALIGN_RIGHT, 5)

        zero_box = wx.BoxSizer(wx.HORIZONTAL)
        self.zero_flag =  wx.StaticText(self.box, label="Zero:", style=wx.ALIGN_RIGHT)
        self.zero_led = LED(self.box, light_color, dark_color)
        zero_box.Add(self.zero_flag,0, wx.ALL|wx.ALIGN_RIGHT, 5)
        zero_box.Add(self.zero_led,0, wx.ALL|wx.ALIGN_RIGHT, 5)

        vertical_box.Add(carry_box,1,wx.EXPAND|wx.ALIGN_RIGHT)
        vertical_box.Add(zero_box, 1, wx.EXPAND|wx.ALIGN_RIGHT)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_get_flags, 'FlagValues')

    def set_in_display_flag(self):
        return True

    def set_out_display_flag(self):
        return True

    def clear_display_flags(self):
        return True

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.carry = False
        self.zero = False
        self.on_clock()

    def on_get_flags(self, new_carry, new_zero):
        self.set_in_display_flag()
        self.carry = new_carry
        self.zero = new_zero
        self.display_flags()

    def display_flags(self):
        self.carry_led.light(self.carry)
        self.zero_led.light(self.zero)