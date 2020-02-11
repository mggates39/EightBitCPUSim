import wx
import wx.gizmos as gizmos
from pubsub import pub

from GuiComponents.Led import LED


class LEDSegment(wx.Panel):
    def __init__(self, parent, led_color='#36ff27', background_color='#077100', topic=None):
        wx.Panel.__init__(self, parent, size=(10, 1))
        self.parent = parent
        self.led_color = led_color
        self.background_color = background_color
        self.value = 0

        pos = wx.DefaultPosition
        size = (100,50) #wx.DefaultSize
        style = gizmos.LED_ALIGN_RIGHT  # | gizmos.LED_DRAW_FADED
        self.segment = gizmos.LEDNumberCtrl(self, -1, pos, size, style)
        # default colours are green on black
        self.segment.SetBackgroundColour(background_color)
        self.segment.SetForegroundColour(led_color)
        self.segment.SetValue('0')

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.segment)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        if topic is not None:
            pub.subscribe(self.set_value, topic)

    def set_value(self, new_value: int) -> None:
        """
        Set the value to be displayed by the 7 segment LED display.
        :type new_value: int
        :rtype: None
        """

        if self.value != new_value:
            self.value = new_value
            self.segment.SetValue("{}".format(self.value))
