import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class Accumulator(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(150, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Accumulator", wx.DefaultPosition, (150, 75))
        self.value = 0
        self.buffer = 0
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="acc.set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.AccIn')
        pub.subscribe(self.on_out, 'CPU.AccOut')

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
        pub.sendMessage('acc.set_value', new_value=self.value)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage('acc.set_value', new_value=self.value)
        pub.sendMessage('alu.set_value_1', new_value=self.value)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)
