import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class CPU(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(80, 110))

        self.parent = parent
        self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, e):

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
        self.sel = 0
        self.cpu = None
        self.slider = None
        self.blue_leds = None
        self.green_leds = None
        self.orange_leds = None
        self.red_leds = None

        self.init_ui()

    def init_ui(self):
        self.sel = 0

        panel = wx.Panel(self)
        center_panel = wx.Panel(panel)
        right_panel = wx.Panel(panel)

        self.cpu = CPU(center_panel)

        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.slider = wx.Slider(panel, value=self.sel, maxValue=100, size=(-1, 100),
                                style=wx.VERTICAL | wx.SL_INVERSE)
        self.slider.SetFocus()

        self.blue_leds = LEDArray(right_panel, 8, '#0065ef', '#00075f', topic='cpu.slide')
        self.green_leds = LEDArray(right_panel, 8, topic='cpu.slide')
        self.orange_leds = LEDArray(right_panel, 8, '#ef7b00', '#5f3700', topic='cpu.slide')
        self.red_leds = LEDArray(right_panel, 8, '#ef0600', '#5b0004', topic='cpu.slide')

        vertical_box.Add(self.blue_leds, 1, wx.ALIGN_CENTER | wx.EXPAND)
        vertical_box.Add(self.green_leds, 1, wx.ALIGN_CENTER | wx.EXPAND)
        vertical_box.Add(self.orange_leds, 1, wx.ALIGN_CENTER | wx.EXPAND)
        vertical_box.Add(self.red_leds, 1, wx.ALIGN_CENTER | wx.EXPAND)
        right_panel.SetSizer(vertical_box)
        right_panel.SetAutoLayout(1)
        vertical_box.Fit(right_panel)

        horizontal_box.Add(center_panel, 0, wx.LEFT | wx.TOP, 20)
        horizontal_box.Add(self.slider, 0, wx.LEFT | wx.TOP, 30)
        horizontal_box.Add(right_panel, 1, wx.LEFT | wx.TOP | wx.EXPAND, 30)

        self.Bind(wx.EVT_SCROLL, self.on_scroll)

        panel.SetSizer(horizontal_box)
        panel.SetAutoLayout(1)
        horizontal_box.Fit(panel)

        self.SetTitle("CPU")
        self.Centre()

    def on_scroll(self, e):
        self.sel = e.GetInt()
        self.cpu.Refresh()
        pub.sendMessage('cpu.slide', new_value=self.sel)


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
