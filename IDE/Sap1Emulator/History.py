import wx
from pubsub import pub

class ExecutionHistory(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(400, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Execution History", wx.DefaultPosition, (400,75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(nmSizer)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self.box, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'tick', width=50)
        self.list.InsertColumn(1, 'ring', width=50)
        self.list.InsertColumn(2, 'control', width=200)
        self.list.InsertColumn(3, 'flags', width=100)

        hbox.Add(self.list, 1, wx.EXPAND)
        nmSizer.Add(hbox, 1, wx.EXPAND)
