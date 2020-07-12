import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedArray import MODE_HEX


class ProgramCounter(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 100))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Program Counter", wx.DefaultPosition, (200, 100))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(40, 75))
        self.increment_indicator = wx.StaticText(self.panel, label="C+")
        self.jump_indicator = wx.StaticText(self.panel, label="Jmp")
        self.read_indicator = wx.StaticText(self.panel, label="CO")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.increment_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.jump_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        self.leds = LEDArray(self.box, 16, topic="pc.set_value", size=10, mode=MODE_HEX)

        horizontal_box.Add(self.leds, 1, wx.ALL | wx.EXPAND, 10)
        horizontal_box.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_jump, 'CPU.PcJump')
        pub.subscribe(self.on_inc, 'CPU.PcInc')
        pub.subscribe(self.on_out, 'CPU.PcOut')
        pub.subscribe(self.on_out_low, 'CPU.PcOutLow')
        pub.subscribe(self.on_out_high, 'CPU.PcOutHigh')

    def set_jmp_display_flag(self):
        self.jump_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_inc_display_flag(self):
        self.increment_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.increment_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.jump_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.on_clock()
        pub.sendMessage('pc.set_value', new_value=self.value)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_jump(self):
        self.value = self.buffer
        self.set_jmp_display_flag()
        pub.sendMessage('pc.set_value', new_value=self.value)

    def on_inc(self):
        self.value += 1
        self.set_inc_display_flag()
        pub.sendMessage('pc.set_value', new_value=self.value)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)

    def on_out_low(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=(self.value & 0xFF))

    def on_out_high(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=((self.value >> 8) & 0xFF))
