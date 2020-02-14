import wx

test = [('0x0:', '00011110'),
        ('0x1:', '00101111'),
        ('0x2:', '11100000'),
        ('0x3:', '11110000'),
        ('0x4:', '00000000'),
        ('0x5:', '00000000'),
        ('0x6:', '00000000'),
        ('0x7:', '00000000'),
        ('0x8:', '00000000'),
        ('0x9:', '00000000'),
        ('0xA:', '00000000'),
        ('0xB:', '00000000'),
        ('0xC:', '00000000'),
        ('0xD:', '00000000'),
        ('0xE:', '00011100'),
        ('0xF:', '00001110')]


class Memory(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "Memory", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self.box, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Addr', width=50)
        self.list.InsertColumn(1, 'Value', width=100)

        self.load_data(test)

        hbox.Add(self.list, 1, wx.EXPAND)
        nmSizer.Add(hbox, 1, wx.EXPAND)
        self.SetSizer(nmSizer)

    def load_data(self, data):
        self.list.DeleteAllItems()
        idx = 0

        for i in data:
            index = self.list.InsertItem(idx, i[0])
            self.list.SetItem(index, 1, i[1])
            idx += 1
