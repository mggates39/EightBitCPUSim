import wx
from pubsub import pub

steps = [['CPU.Clock',
          'CPU.PcOut',
          'CPU.MarIn'],

         ['CPU.Clock',
          'CPU.MemOut',
          'CPU.IrIn',
          'CPU.PcInc'],

         ['CPU.Clock',
          'CPU.IrOut',
          'CPU.MarIn'],

         ['CPU.Clock',
          'CPU.MemOut',
          'CPU.AccIn'],

         ['CPU.Clock',
          'CPU.AccOut',
          'CPU.OutputWrite'],

         ['CPU.Clock',
          'CPU.Halt']
         ]


class Clock(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 75))
        self.parent = parent
        self.index = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (250, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.clock = wx.Button(self.box, -1, "Step")
        self.reset = wx.Button(self.box, -1, "Reset")

        vertical_box.Add(self.clock, 1, wx.ALIGN_CENTER, 10)
        vertical_box.Add(self.reset, 1, wx.ALIGN_CENTER, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_halt, 'CPU.Halt')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        self.clock.Bind(wx.EVT_BUTTON, self.on_click_clock)
        self.reset.Bind(wx.EVT_BUTTON, self.on_click_reset)

    def on_reset(self):
        self.index = 0
        self.clock.Enable(True)

    def on_halt(self):
        self.clock.Enable(False)

    def on_click_clock(self, e):
        microcode = steps[self.index]
        for send in microcode:
            pub.sendMessage(send)
        self.index += 1

    def on_click_reset(self, e):
        pub.sendMessage('CPU.Reset')
