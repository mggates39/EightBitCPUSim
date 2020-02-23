import wx

from GuiComponents.ControlLedArray import ControlLedArray
from Sap2Emulator.MicroCode import control_messages


class ControlLogic(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Control Logic", wx.DefaultPosition, (200, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        cm1 = control_messages[0:17]
        cm2 = control_messages[17:]

        self.leds1 = ControlLedArray(self.box, '#0065ef', '#00075f', cm1)
        self.leds2 = ControlLedArray(self.box, '#0065ef', '#00075f', cm2)

        vertical_box.Add(self.leds1, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        vertical_box.Add(self.leds2, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        static_box_sizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)
