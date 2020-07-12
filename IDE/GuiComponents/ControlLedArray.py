import wx
from pubsub import pub

from GuiComponents.ControlLed import ControlLed


class ControlLedArray(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100', control_messages=None, size: int = 14):
        wx.Panel.__init__(self, parent, size=(10, 1))
        if control_messages is None:
            control_messages = []
        self.parent = parent
        self.light_color = light_color
        self.dark_color = dark_color
        self.leds = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        led_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for message in control_messages:
            led = ControlLed(self, light_color, dark_color, topic=message["topic"], label=message["label"], size=size)
            led_sizer.Add(led, 1, wx.ALL | wx.EXPAND, 1)
            self.leds.append(led)
        self.sizer.Add(led_sizer, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        pub.subscribe(self.reset_leds, "CPU.ClearControl")

    def reset_leds(self) -> None:
        for led in self.leds:
            led.dark()
