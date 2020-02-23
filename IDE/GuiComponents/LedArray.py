"""
    LedArray.py
    -----------

    This module contains the LEDArray Class.
"""

import wx
from pubsub import pub

from GuiComponents.Led import LED


class LEDArray(wx.Panel):
    """
    This class implements an array of n LEDs with a label.
    The label is the value being displayed by the LEDs.
    """

    def __init__(self, parent, number_leds, light_color='#36ff27', dark_color='#077100', topic=None):
        """
        Create the string of LEDs and put a label underneath.  If a topic is provided it will
        subscribe to the topic and update the display everytime it receives a message.
        It will also subscribe to topic + "_label" to allow the lable to be overridden.

        :param parent: anel that will contain the array of LEDs.
        :param number_leds: How many LEDs to display.
        :param light_color: Color of the lit LEDs. Defaults to light green.
        :param dark_color: Color of the dark LEDs. Defaults to dark green.
        :param topic: pyPubSub topic that will change the value to display
        """
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.light_color = light_color
        self.dark_color = dark_color
        self.number_leds = number_leds
        self.value = 0
        self.leds = []
        self.label = wx.StaticText(self, label="0", style=wx.ALIGN_CENTRE)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        led_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(0, number_leds):
            led = LED(self, light_color, dark_color)
            led_sizer.Add(led, 1, wx.ALL, 1)
            self.leds.append(led)
        self.sizer.Add(led_sizer, 1, wx.ALIGN_CENTER)
        self.sizer.Add(self.label, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        if topic is not None:
            pub.subscribe(self.set_value, topic)
            pub.subscribe(self.set_label, topic + "_label")

    def set_value(self, new_value: int) -> None:
        """
        Set the value to be displayed by the LED Array.

        :param new_value: New value to display in the LEDs.
        """
        i = self.number_leds - 1
        if self.value != new_value:
            self.value = new_value
            for led in self.leds:
                if ((2 ** i) & new_value) == (2 ** i):
                    led.light(True)
                else:
                    led.light(False)
                i = i - 1
            self.label.SetLabel("{}".format(new_value))
            self.sizer.Layout()

    def set_label(self, new_label: str) -> None:
        """
        Set the value to be displayed by the LED Array.

        :param new_label: Value to display below the array of LEDs
        """
        self.label.SetLabel("{}".format(new_label))
        self.sizer.Layout()
