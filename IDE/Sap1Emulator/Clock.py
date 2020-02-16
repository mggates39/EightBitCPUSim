import wx
from pubsub import pub


class Clock(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 100))
        self.parent = parent
        self.index = 0
        self.halted = False
        self.speed = 100
        self.timer = wx.Timer(self)
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (250, 100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.start_clock = wx.Button(self.box, -1, "Start")
        self.stop_closk = wx.Button(self.box, -1, "stop")
        self.stop_closk.Enable(False)
        self.single_step = wx.Button(self.box, -1, "Step")
        self.slider = wx.Slider(self.box, value=self.speed, maxValue=1000, minValue=5, size=(200, 20),
                                style=wx.HORIZONTAL)

        horizontal_box.Add(self.start_clock, 1, wx.EXPAND | wx.ALL, 2)
        horizontal_box.Add(self.stop_closk, 1, wx.EXPAND | wx.ALL, 2)
        horizontal_box.Add(self.single_step, 1, wx.EXPAND | wx.ALL, 2)

        vertical_box.Add(horizontal_box, 1, wx.EXPAND)
        vertical_box.Add(self.slider, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_halt, 'CPU.Halt')
        pub.subscribe(self.on_reset, 'CPU.Reset')

        self.start_clock.Bind(wx.EVT_BUTTON, self.on_start_clock)
        self.stop_closk.Bind(wx.EVT_BUTTON, self.on_stop_clock)
        self.single_step.Bind(wx.EVT_BUTTON, self.on_click_clock)
        self.Bind(wx.EVT_TIMER, self.on_click_clock, self.timer)
        self.Bind(wx.EVT_SCROLL, self.on_scroll)

    def on_reset(self):
        self.index = 0
        self.halted = False
        self.start_clock.Enable(True)
        self.stop_closk.Enable(False)
        self.single_step.Enable(True)
        if self.timer.IsRunning():
            self.timer.Stop()

    def on_halt(self):
        self.halted = True
        self.start_clock.Enable(False)
        self.stop_closk.Enable(False)
        self.single_step.Enable(False)
        if self.timer.IsRunning():
            self.timer.Stop()

    def on_start_clock(self, e):
        self.start_clock.Enable(False)
        self.stop_closk.Enable(True)
        self.single_step.Enable(False)
        self.timer.Start(1005-self.speed)

    def on_stop_clock(self, e):
        if self.timer.IsRunning():
            self.timer.Stop()

        self.start_clock.Enable(True)
        self.stop_closk.Enable(False)
        self.single_step.Enable(True)

    def on_click_clock(self, e):
        pub.sendMessage("CPU.ClearContorl")
        pub.sendMessage('CPU.Clock')

    def on_scroll(self, e):
        self.speed = e.GetInt()
        self.timer.Start(1005 - self.speed)

