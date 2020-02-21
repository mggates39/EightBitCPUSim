import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class Accumulator(wx.Panel):
    def __init__(self, parent, name="A"):
        wx.Panel.__init__(self, parent, size=(150, 75))
        title = name + " Register"
        self.topic_prefix = name + "Reg"
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, title, wx.DefaultPosition, (150, 75))
        self.value = 0
        self.buffer = 0
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.read_indicator = wx.StaticText(self.panel, label=name+"O")
        self.write_indicator = wx.StaticText(self.panel, label=name+"I")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic=self.topic_prefix + ".set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)

        hbox.Add(vertical_box, 1, wx.EXPAND)
        hbox.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(hbox, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.'+self.topic_prefix+'In')
        pub.subscribe(self.on_out, 'CPU.'+self.topic_prefix+'Out')

    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.value = 0
        self.buffer = 0
        self.on_clock()
        pub.sendMessage(self.topic_prefix + ".set_value", new_value=self.value)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage(self.topic_prefix + '.set_value', new_value=self.value)
        pub.sendMessage('alu.set_value_' + self.topic_prefix, new_value=self.value)

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)
