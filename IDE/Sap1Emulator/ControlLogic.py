import wx

from GuiComponents.ControlLedArray import ControlLedArray
from Sap1Emulator.MicroCode import control_messages


class ControlLogic(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Control Logic", wx.DefaultPosition, (200, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = ControlLedArray(self.box, '#0065ef', '#00075f', control_messages)

        vertical_box.Add(self.leds, 1, wx.EXPAND | wx.ALL, 5)

        static_box_sizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)
