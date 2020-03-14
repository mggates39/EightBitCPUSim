import wx
from pubsub import pub

test = [('0x0000:', '00111010'),
        ('0x0001:', '00010000'),
        ('0x0002:', '00000000'),
        ('0x0003:', '01000111'),
        ('0x0004:', '00111010'),
        ('0x0005:', '00001111'),
        ('0x0006:', '00000000'),
        ('0x0007:', '10100000'),
        ('0x0008:', '00110010'),
        ('0x0009:', '00001110'),
        ('0x000A:', '00000000'),
        ('0x000B:', '11010011'),
        ('0x000C:', '00000011'),
        ('0x000D:', '01110110'),
        ('0x000E:', '00000000'),
        ('0x000F:', '00011100'),
        ('0x0010:', '00001110')]


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
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = wx.Panel(self.box, size=(30, 75))
        self.read_indicator = wx.StaticText(self.panel, label="RO")
        self.write_indicator = wx.StaticText(self.panel, label="RI")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        self.list = wx.ListCtrl(self.box, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Addr', width=70)
        self.list.InsertColumn(1, 'Value', width=100)

        self.load_data(test)

        hbox.Add(self.panel, 0, wx.EXPAND)
        hbox.Add(self.list, 1, wx.EXPAND)
        static_box_sizer.Add(hbox, 1, wx.EXPAND)
        self.SetSizer(static_box_sizer)

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
        data = self.reset_data
        self.load_data(data)
        self.list.Select(self.address, 0)
        self.address = 0
        self.on_clock()

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_set_address(self, new_value):
        self.list.Select(self.address, 0)

        self.address = new_value

        self.list.Focus(self.address)
        self.list.Select(self.address)

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        new_data = "{0:08b}".format(self.value)
        new_address = "0x{0:X}:".format(self.address)

        self.data[self.address] = (new_address, new_data)
        self.list.SetItem(self.address, 1, self.data[self.address][1])

    def on_out(self):
        self.set_out_display_flag()
        self.value = int(self.data[self.address][1], 2)
        pub.sendMessage('CPU.ChangeBus', new_value=self.value)
