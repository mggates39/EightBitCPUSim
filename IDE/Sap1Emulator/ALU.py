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
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="alu.set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_a_value, 'alu.set_value_1')
        pub.subscribe(self.on_b_value, 'alu.set_value_2')
        pub.subscribe(self.on_out, 'CPU.AluOut')
        pub.subscribe(self.on_subtract, 'CPU.AluSub')
        pub.subscribe(self.on_save_flags, 'CPU.SaveFlag')


    def set_sub_display_flag(self):
        return True

    def set_out_display_flag(self):
        return True

    def clear_display_flags(self):
        return True

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
        if self.result == 9:
            self.zero = True
        else:
            self.zero = False
        pub.sendMessage('alu.set_value', new_value=self.result)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.result)

    def on_save_flags(self):
        pub.sendMessage("FlagValues", new_carry=self.carry, new_zero=self.zero)