"""
    Led.py
    ------

    This module contains the LED class.
"""

import wx


class LED(wx.Panel):
    def __init__(self, parent: wx.Panel, light_color: str = '#36ff27', dark_color: str = '#077100') -> None:
        """
        This class creates a visual representation of an LED that can be turned on and off

        :param parent: Panel that will hold the LED
        :param light_color: Color for lit LED default to light green
        :param dark_color: Color for dark (unlit) LED defautls to dark green
        """
        wx.Panel.__init__(self, parent, size=(14, 14))
        self.parent = parent
        # self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.lit = False
        self.light_color = light_color
        self.dark_color = dark_color

    def light(self, on_off: bool) -> None:
        """
        Turn the LED On or Off

        :param on_off: True to turn on the LED
        """
        self.lit = on_off
        self.Refresh()

    def on_paint(self, e):
        """
        Implement wxPython Paint Event.
        Chooses the color of the LED based on whether it is lit.

        :param e: event
        """
        dc = wx.PaintDC(self)

        if self.lit:
            color = self.light_color
        else:
            color = self.dark_color

        dc.SetBrush(wx.Brush(color))
        dc.DrawEllipse(0, 0, 13, 13)
