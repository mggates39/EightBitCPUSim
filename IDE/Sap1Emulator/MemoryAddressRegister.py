import wx
from pubsub import pub

class MemoryAddressRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Memory Address Register", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

