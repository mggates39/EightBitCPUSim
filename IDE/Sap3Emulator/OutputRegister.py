import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedArray import MODE_DEC
from GuiComponents.LedArray import MODE_HEX
from GuiComponents.LedSegments import LEDSegment


class OutputRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 100))
        self.parent = parent
        self.value = 0
        self.select = 0
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Output Register", wx.DefaultPosition, (100, 100))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.write_indicator = wx.StaticText(self.panel, label="OI")
        self.select_indicator = wx.StaticText(self.panel, label="OS")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.select_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.segment = LEDSegment(self.box, 'blue', None, topic='out.set_value', mode=MODE_HEX)
        self.leds = LEDArray(self.box, 8, topic="out.set_value", size=10, mode=MODE_HEX)

        vertical_box.Add(self.segment, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        hbox.Add(vertical_box, 1, wx.EXPAND)
        hbox.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(hbox, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_output_select, 'CPU.OutputSelect')
        pub.subscribe(self.on_out, 'CPU.OutputWrite')

        pub.sendMessage('out.set_value', new_value=self.value)

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_select_display_flag(self):
        self.select_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.select_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_output_select(self):
        self.select = self.buffer
        self.set_select_display_flag()

    def on_out(self):
        self.value = self.buffer
        self.set_in_display_flag()
        if self.select == 2:
            self.segment.set_mode(new_mode=MODE_DEC)
            self.leds.set_mode(new_mode=MODE_DEC)
            pub.sendMessage('out.set_value', new_value=self.value)
        elif self.select == 3:
            self.segment.set_mode(new_mode=MODE_HEX)
            self.leds.set_mode(new_mode=MODE_HEX)
            pub.sendMessage('out.set_value', new_value=self.value)
        else:
            print("{}".format(self.value))


    def on_reset(self):
        self.value = 0
        self.select = 0
        self.buffer = 0
        self.clear_display_flags()
        pub.sendMessage('out.set_value', new_value=self.value)

    def on_clock(self):
        self.clear_display_flags()
