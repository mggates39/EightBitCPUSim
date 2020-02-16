import wx
from pubsub import pub


class Clock(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 100))
        self.parent = parent
        self.index = 0
        self.halted = False
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (250, 100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.clock = wx.Button(self.box, -1, "Step")

        vertical_box.Add(self.clock, 1, wx.ALIGN_CENTER, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_halt, 'CPU.Halt')
        pub.subscribe(self.on_reset, 'CPU.Reset')

        self.clock.Bind(wx.EVT_BUTTON, self.on_click_clock)

    def on_reset(self):
        self.index = 0
        self.halted = False
        self.clock.Enable(True)

    def on_halt(self):
        self.halted = True
        self.clock.Enable(False)

    def on_click_clock(self, e):
        pub.sendMessage("CPU.ClearContorl")
        pub.sendMessage('CPU.Clock')

