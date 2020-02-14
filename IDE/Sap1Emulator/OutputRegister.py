import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedSegments import LEDSegment


class OutputRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 100))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Output Register", wx.DefaultPosition, (100, 100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.segment = LEDSegment(self.box, 'blue', None, topic='out.set_value')
        self.leds = LEDArray(self.box, 8, topic="out.set_value")

        vertical_box.Add(self.segment, 1, wx.ALIGN_CENTER | wx.EXPAND, 20)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_out, 'CPU.OutputWrite')

    def set_out_display_flag(self):
        return True

    def clear_display_flags(self):
        return True

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_out(self):
        self.value = self.buffer
        self.set_out_display_flag()
        pub.sendMessage('out.set_value', new_value=self.value)

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.on_clock()
        self.on_out()

    def on_clock(self):
        self.clear_display_flags()
