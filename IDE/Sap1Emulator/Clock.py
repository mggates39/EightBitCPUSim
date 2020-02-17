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
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.start_clock = wx.Button(self.box, -1, "Start")
        self.stop_closk = wx.Button(self.box, -1, "stop")
        self.stop_closk.Enable(False)
        self.single_step = wx.Button(self.box, -1, "Step")
        self.slider = wx.Slider(self.box, value=self.speed, maxValue=1000, minValue=5, size=(200, 20),
                                style=wx.HORIZONTAL)

        hbox.Add(self.start_clock, 1, wx.EXPAND)
        hbox.Add(self.stop_closk, 1, wx.EXPAND)
        hbox.Add(self.single_step, 1, wx.EXPAND)

        vertical_box.Add(hbox, 1, wx.EXPAND)
        vertical_box.Add(self.slider, 1, wx.ALIGN_CENTER | wx.TOP, 5)

        self.panel = wx.Panel(self.box, size=( 40, 75))
        self.halt_indicator = wx.StaticText(self.panel, label="HLT")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.halt_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        horizontal_box.Add(self.panel, 0, wx.EXPAND)
        horizontal_box.Add(vertical_box, 1, wx.EXPAND)

        nmSizer.Add(horizontal_box, 1, wx.EXPAND)

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
        self.halt_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.start_clock.Enable(True)
        self.stop_closk.Enable(False)
        self.single_step.Enable(True)
        if self.timer.IsRunning():
            self.timer.Stop()

    def on_halt(self):
        self.halted = True
        self.halt_indicator.SetForegroundColour((0, 0, 255))  # set text color
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

