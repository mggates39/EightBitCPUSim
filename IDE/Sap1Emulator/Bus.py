import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray

class Bus(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Bus", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        light_color='#36ff27'
        dark_color='#077100'
        self.value = 0
        self.leds = LEDArray(self.box, 8, light_color, dark_color, 'bus.set_lights')
        nmSizer.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALIGN_TOP | wx.EXPAND)
        self.SetSizer(nmSizer)

        pub.subscribe(self.SetValue, "CPU.ChangeBus")

    def SetValue(self, new_value):
        if new_value != self.value:
            self.value = new_value
            pub.sendMessage('bus.set_lights', new_value=self.value)
            pub.sendMessage("CPU.BusChanged", new_value=self.value)


