import wx
from pubsub import pub

from GuiComponents.LedArray import LED
from Sap1Emulator.MicroCode import control_messages


class ControlLed(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100', topic=None, label=None):
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.light_color = light_color
        self.dark_color = dark_color
        self.label = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.led = LED(self, light_color, dark_color)
        if label is not None:
            self.label = wx.StaticText(self, label=label, style=wx.ALIGN_CENTRE)
            self.sizer.Add(self.label, 1, wx.ALIGN_CENTRE | wx.EXPAND)
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


class ControlLedArray(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100'):
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.light_color = light_color
        self.dark_color = dark_color
        self.leds = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        led_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in control_messages:
            message = control_messages[i]
            led = ControlLed(self, light_color, dark_color, topic=message["topic"], label=message["label"])
            led_sizer.Add(led, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 1)
            self.leds.append(led)
        self.sizer.Add(led_sizer, 1, wx.ALIGN_CENTER | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        pub.subscribe(self.reset_leds, "CPU.ClearContorl")

    def reset_leds(self) -> None:
        for led in self.leds:
            led.dark()


class ControlLogic(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Control Logic", wx.DefaultPosition, (200, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = ControlLedArray(self.box, '#0065ef', '#00075f')

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)
