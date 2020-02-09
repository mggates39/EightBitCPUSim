import wx

class LED(wx.Panel):
    def __init__(self, parent, light_color='#36ff27', dark_color='#077100'):
        wx.Panel.__init__(self, parent, size=(15, 15))
        self.parent = parent
        # self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.lit = False
        self.light_color = light_color
        self.dark_color = dark_color

    def light(self, on_off: bool):
        self.lit = on_off
        self.Refresh()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)

        if self.lit:
            color = self.light_color
        else:
            color = self.dark_color

        dc.SetBrush(wx.Brush(color))
        dc.DrawEllipse(0, 0, 14, 14)
