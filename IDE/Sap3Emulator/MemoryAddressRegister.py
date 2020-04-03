import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedArray import MODE_HEX


class MemoryAddressRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 100))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.break_points = []
        self.box = wx.StaticBox(self, wx.ID_ANY, "Memory Address Register", wx.DefaultPosition, (250, 100))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.write_indicator = wx.StaticText(self.panel, label="MI")
        self.increment_indicator = wx.StaticText(self.panel, label="M+")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.increment_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        self.leds = LEDArray(self.box, 16, topic="mar.set_value", size=10, mode=MODE_HEX)

        horizontal_box.Add(self.panel, 0, wx.EXPAND)
        horizontal_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.MarIn')
        pub.subscribe(self.on_inc, 'CPU.MarInc')
        pub.subscribe(self.set_breakpoint, 'mar.set_break')
        pub.subscribe(self.clear_breakpoint, 'mar.clear_break')

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_inc_display_flag(self):
        self.increment_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.increment_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.on_clock()
        pub.sendMessage('mar.set_value', new_value=self.value)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def set_breakpoint(self, address):
        if address not in self.break_points:
            self.break_points.append(address)

    def clear_breakpoint(self, address):
        if address in self.break_points:
            self.break_points.remove(address)

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage('mar.set_value', new_value=self.value)
        pub.sendMessage('mem.set_address', new_value=self.value)
        # Execute breakpoint if accessing break boint memory
        if self.value in self.break_points:
            pub.sendMessage('CPU.Break')

    def on_inc(self):
        self.value += 1
        self.set_inc_display_flag()
        pub.sendMessage('mar.set_value', new_value=self.value)
        pub.sendMessage('mem.set_address', new_value=self.value)
        # Execute breakpoint if accessing break boint memory
        if self.value in self.break_points:
            pub.sendMessage('CPU.Break')
