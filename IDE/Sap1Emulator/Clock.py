import wx
from pubsub import pub

class Clock(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (00, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

