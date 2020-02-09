import wx

from GuiComponents.Led_Array import LED_Array


class CPU(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(80, 110))

        self.parent = parent
        self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e):

        dc = wx.PaintDC(self)

        dc.SetDeviceOrigin(0, 100)
        dc.SetAxisOrientation(True, True)

        pos = self.parent.GetParent().GetParent().sel
        rect = pos / 5

        for i in range(1, 21):

            if i > rect:
                if i > 17:
                    color = '#8b0000'
                else:
                    color = '#075100'
            else:
                if i > 17:
                    color = '#ff4500'
                else:
                    color = '#36ff27'

            dc.SetBrush(wx.Brush(color))
            dc.DrawRectangle(10, i * 4, 30, 5)
            dc.DrawRectangle(41, i * 4, 30, 5)


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        self.sel = 0

        panel = wx.Panel(self)
        centerPanel = wx.Panel(panel)
        rightPanel = wx.Panel(panel)

        self.cpu = CPU(centerPanel)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.slider = wx.Slider(panel, value=self.sel, maxValue=100, size=(-1, 100),
                                style=wx.VERTICAL | wx.SL_INVERSE)
        self.slider.SetFocus()

        self.leds = LED_Array(rightPanel, 8)

        hbox.Add(centerPanel, 0, wx.LEFT | wx.TOP, 20)
        hbox.Add(self.slider, 0, wx.LEFT | wx.TOP, 30)
        hbox.Add(rightPanel, 0, wx.LEFT | wx.TOP, 40)

        self.Bind(wx.EVT_SCROLL, self.OnScroll)

        panel.SetSizer(hbox)

        self.SetTitle("CPU")
        self.Centre()

    def OnScroll(self, e):
        self.sel = e.GetInt()
        self.cpu.Refresh()
        self.leds.SetValue(self.sel)


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
