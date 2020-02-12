import wx
from pubsub import pub

class Clock(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(75, 199))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (75,100))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

