import wx
from pubsub import pub

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
        self.data = []
        self.reset_data = []
        self.address = 0
        self.buffer = 0
        self.value = 0
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

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.MemIn')
        pub.subscribe(self.on_out, 'CPU.MemOut')
        pub.subscribe(self.on_set_address, 'mem.set_address')

    def load_data(self, data):
        self.list.DeleteAllItems()
        self.data = []
        self.reset_data = []
        idx = 0

        for i in data:
            self.data.append(i)
            self.reset_data.append(i)
            index = self.list.InsertItem(idx, i[0])
            self.list.SetItem(index, 1, i[1])
            idx += 1

    def set_in_display_flag(self):
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
        data = self.reset_data
        self.load_data(data)
        self.on_set_address(0)
        self.on_clock()

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_set_address(self, new_value):
        self.address = new_value & 15
        self.list.Focus(self.address)
        self.list.Select(self.address)

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()

        self.data[self.address][1] = "0:08b".format(self.value)
        self.list.SetItem(self.address, 1, self.data[self.address][1] )

    def on_out(self):
        self.set_out_display_flag()
        self.value = int( self.data[self.address][1], 2)
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)
