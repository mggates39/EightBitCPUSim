"""
    Bus.py
    ------

    This module contains the Eight Bit Data buse implementation and display.
"""

import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class Bus(wx.Panel):
    """
    The Bus class implements the data bus data passing and display inside a wxPython Panel.
    """

    def __init__(self, parent):
        """
        Create a new Bus Panel

        :param parent: Panel that will contain this Bus Panel
        """
        wx.Panel.__init__(self, parent, size=(275, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Bus", wx.DefaultPosition, (300, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        light_color = '#36ff27'
        dark_color = '#077100'
        self.value = 0
        self.leds = LEDArray(self.box, 16, light_color, dark_color, 'bus.set_lights', size=10)
        self.pan = wx.Panel(self.box)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALIGN_TOP | wx.ALL | wx.EXPAND, 10)
        vertical_box.Add(self.pan, 1, wx.ALL | wx.EXPAND)
        static_box_sizer.Add(vertical_box, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_write, "CPU.ChangeBus")

    def on_bus_write(self, new_value: object) -> None:
        """
        Put a new value on the data bus and tell everyone that is interested that there is new data.
        Also update the LED array with the new data value.

        :param new_value: The new value to be written on to the bus
        """
        if new_value != self.value:
            self.value = new_value
            pub.sendMessage('bus.set_lights', new_value=self.value)
            pub.sendMessage('CPU.BusChanged', new_value=self.value)

    def on_reset(self) -> None:
        """
        Reset the bus to all zeros.
        """
        self.value = 0
        pub.sendMessage('bus.set_lights', new_value=self.value)
