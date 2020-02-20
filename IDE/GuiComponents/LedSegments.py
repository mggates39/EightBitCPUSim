"""
    LedEDSegment.py
    ------

    This module contains the seven segment lED display.
"""

import wx
import wx.gizmos as gizmos
from pubsub import pub


class LEDSegment(wx.Panel):
    """
    The LEDSegment class implements a seven segement display
    """
    def __init__(self, parent, led_color='#36ff27', background_color='#077100', topic=None):
        """

        :param parent: Panel that will hold the Seven Segment display
        :param led_color: Color of the LED segments.  Defaults to light green
        :param background_color: Color of the background of the display.  Defaults to Dark Green
        :param topic: pyPubSub topic that will change the value to display
        """
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.led_color = led_color
        self.background_color = background_color
        self.value = 0

        pos = wx.DefaultPosition
        size = (100, 50)  # wx.DefaultSize
        style = gizmos.LED_ALIGN_RIGHT  # | gizmos.LED_DRAW_FADED
        self.segment = gizmos.LEDNumberCtrl(self, -1, pos, size, style)
        # default colours are green on black
        self.segment.SetBackgroundColour(background_color)
        self.segment.SetForegroundColour(led_color)
        self.segment.SetValue('0')

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.segment, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        if topic is not None:
            pub.subscribe(self.set_value, topic)

    def set_value(self, new_value: int) -> None:
        """
        Set the value to be displayed by the 7 segment LED display.
        :param new_value: new value to display
        """

        if self.value != new_value:
            self.value = new_value
            self.segment.SetValue("{}".format(self.value))
