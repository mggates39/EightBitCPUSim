import wx
from pubsub import pub

from GuiComponents.LedArray import LED


class ControlLed(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100', topic=None, label=None, size:int = 14):
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.light_color = light_color
        self.dark_color = dark_color
        self.label = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.led = LED(self, light_color, dark_color, size)
        if label is not None:
            self.label = wx.StaticText(self, label=label, style=wx.ALIGN_CENTER)
            self.sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.EXPAND)
        self.sizer.Add(self.led, 1, wx.ALIGN_CENTER | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.sizer.Layout()

        if topic is not None:
            pub.subscribe(self.light, topic)

    def light(self) -> None:
        self.led.light(True)

    def dark(self) -> None:
        self.led.light(False)
