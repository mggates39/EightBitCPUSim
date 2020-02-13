import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class TempRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Temp Register", wx.DefaultPosition, (100,75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="tmp.set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

