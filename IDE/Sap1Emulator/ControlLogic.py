import wx
from pubsub import pub

from GuiComponents.LedArray import LED

control_messages = {
    0: {"topic": "CPU.Halt", "label": "HLT"},
    1: {"topic": "CPU.MarIn", "label": "MI"},
    2: {"topic": "CPU.MemIn", "label": "RI"},
    3: {"topic": "CPU.MemOut", "label": "RO"},
    4: {"topic": "CPU.IrIn", "label": "II"},
    5: {"topic": "CPU.IrOut", "label": "IO"},
    6: {"topic": "CPU.AccIn", "label": "AI"},
    7: {"topic": "CPU.AccOut", "label": "AO"},

    8: {"topic": "CPU.AluOut", "label": "EO"},
    9: {"topic": "CPU.AluSub", "label": "SU"},
    10: {"topic": "CPU.TempIn", "label": "BI"},
    11: {"topic": "CPU.OutputWrite", "label": "OI"},

    12: {"topic": "CPU.PcOut", "label": "CO"},
    13: {"topic": "CPU.PcInc", "label": "CI"},
    14: {"topic": "CPU.PcJump", "label": "CJ"},
    15: {"topic": "CPU.FlagIn", "label": "FI"},
    16: {"topic": "CPU.RingReset", "label": "RCR"},
}


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

        pub.subscribe(self.reset_leds,"CPU.ClearContorl")

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
