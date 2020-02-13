import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class ProgramCounter(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Program Counter", wx.DefaultPosition, (200, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="pc.set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)
