import wx


class LED(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100'):
        wx.Panel.__init__(self, parent, size=(14, 14))
        self.parent = parent
        # self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.lit = False
        self.light_color = light_color
        self.dark_color = dark_color

    def light(self, on_off: bool) -> None:
        """Turn the LED On or Off

        Keyword Arguments:
        on_off - True to turn on the LED
        """
        self.lit = on_off
        self.Refresh()

    def on_paint(self, e):
        dc = wx.PaintDC(self)

        if self.lit:
            color = self.light_color
        else:
            color = self.dark_color

        dc.SetBrush(wx.Brush(color))
        dc.DrawEllipse(0, 0, 13, 13)
