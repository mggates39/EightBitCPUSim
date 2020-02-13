import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class InstructionRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Instruction Register", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.HORIZONTAL)

        self.instruction = LEDArray(self.box, 4, topic="ip.set_instruction")
        self.data = LEDArray(self.box, 4, topic="ip.set_data")

        vertical_box.Add(self.instruction, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        vertical_box.Add(self.data, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

