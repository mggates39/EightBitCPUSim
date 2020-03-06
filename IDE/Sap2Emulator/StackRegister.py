import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from Sap2Assembler.Segment import MAX_ADDRESS


class StackRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(350, 100))
        self.parent = parent
        self.value = MAX_ADDRESS - 1
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Stack Register", wx.DefaultPosition, (350, 100))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(40, 75))
        self.write_indicator = wx.StaticText(self.panel, label="SI")
        self.read_indicator = wx.StaticText(self.panel, label="SO")
        self.inc_indicator = wx.StaticText(self.panel, label="Inc")
        self.dec_indicator = wx.StaticText(self.panel, label="Dec")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vbox.Add(self.inc_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vbox.Add(self.dec_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.panel.SetSizer(vbox)

        self.leds = LEDArray(self.box, 16, topic="sp.set_value")

        horizontal_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)
        horizontal_box.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        self.on_reset()

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.SpIn')
        pub.subscribe(self.on_out, 'CPU.SpOut')
        pub.subscribe(self.on_inc, 'CPU.SpInc')
        pub.subscribe(self.on_dec, 'CPU.SpDec')

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_inc_display_flag(self):
        self.inc_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_dec_display_flag(self):
        self.dec_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.inc_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.dec_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.value = MAX_ADDRESS -1
        self.buffer = 0
        self.clear_display_flags()
        pub.sendMessage('sp.set_value', new_value=self.value)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage('sp.set_value', new_value=self.value)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)

    def on_inc(self):
        self.value += 1
        self.set_inc_display_flag()
        pub.sendMessage('sp.set_value', new_value=self.value)

    def on_dec(self):
        self.value -= 1
        self.set_dec_display_flag()
        pub.sendMessage('sp.set_value', new_value=self.value)

