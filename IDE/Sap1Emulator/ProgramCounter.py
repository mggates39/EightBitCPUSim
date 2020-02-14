import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class ProgramCounter(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(250, 75))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Program Counter", wx.DefaultPosition, (250, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 4, topic="pc.set_value")

        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_jump, 'CPU.PcJump')
        pub.subscribe(self.on_inc, 'CPU.PcInc')
        pub.subscribe(self.on_out, 'CPU.PcOut')


    def set_jmp_display_flag(self):
        return True

    def set_inc_display_flag(self):
        return True

    def set_out_display_flag(self):
        return True

    def clear_display_flags(self):
        return True

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

