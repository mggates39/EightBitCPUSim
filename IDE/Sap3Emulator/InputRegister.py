import wx
from pubsub import pub

from GuiComponents.LedSegments import MODE_DEC
from GuiComponents.LedSegments import MODE_HEX
from GuiComponents.LedSegments import LEDSegment


class InputRegister(wx.Panel):
    MODE_ADDR = 0
    MODE_DATA = 1
    MODE_INPUT = 2

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 100))
        self.parent = parent
        self.address_value = '----'
        self.data_value = '--'
        self.select = 0
        self.buffer = 0
        self.mode = None

        self.box = wx.StaticBox(self, wx.ID_ANY, "Input Register", wx.DefaultPosition, (100, 100))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self, size=(30, 75))
        self.request_indicator = wx.StaticText(self.panel, label="NI")
        self.reponse_indicator = wx.StaticText(self.panel, label="NO")
        self.select_indicator = wx.StaticText(self.panel, label="NS")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.request_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.reponse_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.select_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)


        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.addr_segment = LEDSegment(self, 'blue', None, size = (75, 50), topic='in.set_addr_value', mode=MODE_HEX, num_digits=4)
        self.data_segment = LEDSegment(self, 'blue', None, size = (30, 50), topic='in.set_data_value', mode=MODE_HEX, num_digits=2)
        b = wx.Button(self, -1, label='Enter')
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.addr_segment, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.data_segment, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(b, 1, wx.EXPAND | wx.ALL, 5)


        gs = wx.GridSizer(4, 6, 5, 5)
        for row in (('C', 'D', 'E', 'F', 'ADDR', 'DATA'),
                    ('8', '9', 'A', 'B', 'exam', 'dep'),
                    ('4', '5', '6', '7', 'exnxt', 'dpnxt'),
                    ('0', '1', '2', '3', 'exprv', 'dpprv')):
            for label in row:
                b = wx.Button(self, -1, label=label)
                gs.Add(b, 0, wx.EXPAND)
                self.Bind(wx.EVT_BUTTON, self.OnButton, b)


        vertical_box.Add(hbox, 1, wx.EXPAND)
        vertical_box.Add(gs, proportion=1, flag=wx.EXPAND)

        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box.Add(vertical_box, 1, wx.EXPAND)
        horizontal_box.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_input_select, 'CPU.InputSelect')
        pub.subscribe(self.on_read, 'CPU.InputRequest')

        pub.sendMessage('in.set_addr_value', new_value=self.address_value)
        pub.sendMessage('in.set_data_value', new_value=self.data_value)

    def set_request_display_flag(self):
        self.request_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_response_display_flag(self):
        self.reponse_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_select_display_flag(self):
        self.select_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.request_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.reponse_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.select_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def deposit_memory(self):
        pub.sendMessage("CPU.ClearControl")
        pub.sendMessage('CPU.Clock')
        pub.sendMessage('ir.ring', tick=-1, cycle=-1, ring=-1)
        pub.sendMessage('CPU.ChangeBus', new_value=self.address_value)
        pub.sendMessage('CPU.MarIn')
        pub.sendMessage('CPU.ChangeBus', new_value=self.data_value)
        pub.sendMessage('CPU.MemIn')

    def examine_memory(self):
        pub.sendMessage("CPU.ClearControl")
        pub.sendMessage('CPU.Clock')
        pub.sendMessage('ir.ring', tick=-1, cycle=-1, ring=-1)
        pub.sendMessage('CPU.ChangeBus', new_value=self.address_value)
        pub.sendMessage('CPU.MarIn')
        pub.sendMessage('CPU.MemOut')
        self.data_value = self.buffer
        pub.sendMessage('in.set_data_value', new_value=self.data_value)

    def respond_input(self):
        self.clear_display_flags()
        self.set_response_display_flag()
        self.mode = None
        pub.sendMessage('CPU.ChangeBus', new_value=self.data_value)
        pub.sendMessage('CPU.InputResponse')


    def OnButton(self, evt):
        label = evt.GetEventObject().GetLabel()

        if label == 'ADDR' and self.mode != self.MODE_INPUT:
            self.mode = self.MODE_ADDR
            if self.address_value == '----':
                self.address_value = 0
        elif label == 'DATA' and self.mode != self.MODE_INPUT:
            self.mode = self.MODE_DATA
            if self.data_value == '--':
                self.data_value = 0
        elif label == 'exam' and self.mode != self.MODE_INPUT:
            self.examine_memory()
        elif label == 'exnxt' and self.mode != self.MODE_INPUT:
            self.address_value += 1
            pub.sendMessage('in.set_addr_value', new_value=self.address_value)
            self.examine_memory()
        elif label == 'exprv' and self.mode != self.MODE_INPUT:
            self.address_value -= 1
            pub.sendMessage('in.set_addr_value', new_value=self.address_value)
            self.examine_memory()
        elif label == 'dep' and self.mode != self.MODE_INPUT:
            self.deposit_memory()
        elif label == 'dpnxt' and self.mode != self.MODE_INPUT:
            self.address_value += 1
            pub.sendMessage('in.set_addr_value', new_value=self.address_value)
            self.deposit_memory()
        elif label == 'dpprv' and self.mode != self.MODE_INPUT:
            self.address_value -= 1
            pub.sendMessage('in.set_addr_value', new_value=self.address_value)
            self.deposit_memory()
        elif label == 'Enter' and self.mode == self.MODE_INPUT:
            self.respond_input()
        else:
            if self.mode == self.MODE_ADDR:
                new_value = self.address_value << 4
                new_value = new_value | int(label, 16)
                new_value = new_value & 0xFFFF
                self.address_value = new_value
                pub.sendMessage('in.set_addr_value', new_value=self.address_value)

            elif self.mode == self.MODE_DATA or self.mode == self.MODE_INPUT:
                new_value = self.data_value << 4
                new_value = new_value | int(label, 16)
                new_value = new_value & 0xFF
                self.data_value = new_value
                pub.sendMessage('in.set_data_value', new_value=self.data_value)




    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_input_select(self):
        self.select = self.buffer
        self.set_select_display_flag()

    def on_read(self):
        self.set_request_display_flag()
        self.mode = self.MODE_INPUT
        if self.data_value == '--':
            self.data_value = 0
        pub.sendMessage('CPU.Pause')


    def on_reset(self):
        self.address_value = 0
        self.data_value = 0
        self.address_value = '----'
        self.data_value = '--'
        self.mode = None
        self.clear_display_flags()
        pub.sendMessage('in.set_addr_value', new_value=self.address_value)
        pub.sendMessage('in.set_data_value', new_value=self.data_value)

    def on_clock(self):
        self.clear_display_flags()
