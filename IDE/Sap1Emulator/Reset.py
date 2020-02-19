import wx
from pubsub import pub


class Reset(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 100))
        self.parent = parent
        self.index = 0
        self.halted = False
        self.speed = 100
        self.timer = wx.Timer(self)
        self.box = wx.StaticBox(self, wx.ID_ANY, "Reset", wx.DefaultPosition, (250, 100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.resetButton = wx.Button(self.box, wx.ID_ANY, "Reset")
        vertical_box.Add(self.resetButton, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        self.resetButton.Bind(wx.EVT_BUTTON, self.on_click_reset)

    def on_click_reset(self, e):
        pub.sendMessage("CPU.ClearContorl")
        pub.sendMessage('CPU.Reset')