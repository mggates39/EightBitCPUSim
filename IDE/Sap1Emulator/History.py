import wx
from pubsub import pub

class ExecutionHistory(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(400, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Execution History", wx.DefaultPosition, (400,75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

