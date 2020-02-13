import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedSegments import LEDSegment


class OutputRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 100))
        self.parent = parent
        self.value = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Output Register", wx.DefaultPosition, (100, 100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.segment = LEDSegment(self.box, 'black', None, topic='out.set_value')
        self.leds = LEDArray(self.box, 8, topic="out.set_value")

        vertical_box.Add(self.segment, 1, wx.ALIGN_CENTER | wx.EXPAND, 20)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.SetValue, 'CPU.BusChanged')
        pub.subscribe(self.Display, 'CPU.OutputWrite')

    def SetValue(self, new_value):
        if new_value != self.value:
            self.value = new_value

    def Display(self):
        pub.sendMessage('out.set_value', new_value=self.value)
        pub.sendMessage('out.set_value', new_value=self.value)
