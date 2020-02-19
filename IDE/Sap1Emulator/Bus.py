import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray

class Bus(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(175, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Bus", wx.DefaultPosition, (150, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        light_color='#36ff27'
        dark_color='#077100'
        self.value = 0
        self.leds = LEDArray(self.box, 8, light_color, dark_color, 'bus.set_lights')
        self.pan = wx.Panel(self.box)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALIGN_TOP | wx.ALL | wx.EXPAND, 10)
        vertical_box.Add(self.pan, 1, wx.ALL | wx.EXPAND)
        nmSizer.Add(vertical_box, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_write, "CPU.ChangeBus")

    def on_bus_write(self, new_value):
        if new_value != self.value:
            self.value = new_value
            pub.sendMessage('bus.set_lights', new_value=self.value)
            pub.sendMessage('CPU.BusChanged', new_value=self.value)

    def on_reset(self):
        self.value = 0
        pub.sendMessage('bus.set_lights', new_value=self.value)

    def on_clock(self):
        return True