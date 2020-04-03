import wx
from pubsub import pub

from Sap2Emulator.MicroCode import control_messages, decode_messages


class ExecutionHistory(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(400, 75))
        self.parent = parent
        self.last_index = 0
        self.last_control = ""
        self.box = wx.StaticBox(self, wx.ID_ANY, "Execution History", wx.DefaultPosition, (400, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.SetSizer(static_box_sizer)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.list = wx.ListCtrl(self.box, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'tick', width=50)
        self.list.InsertColumn(1, 'cycle', width=50)
        self.list.InsertColumn(2, 'ring', width=50)
        self.list.InsertColumn(3, 'control', width=200)

        hbox.Add(self.list, 1, wx.EXPAND)
        static_box_sizer.Add(hbox, 1, wx.EXPAND)

        for message in control_messages:
            pub.subscribe(self.on_control, message["topic"])

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_start_message, 'ir.ring')

    def on_clock(self):
        self.last_control = ""

    def on_reset(self):
        self.list.DeleteAllItems()
        self.last_index = 0
        self.last_control = ""

    def on_start_message(self, tick, cycle, ring):
        self.last_control = ""
        self.last_index = self.list.InsertItem(0, "{}".format(tick))
        self.list.SetItem(self.last_index, 1, "{}".format(cycle))
        self.list.SetItem(self.last_index, 2, "{}".format(ring))

    def on_control(self, topic=pub.AUTO_TOPIC):
        topic_name = topic.getName()
        if topic_name in decode_messages:
            self.last_control += decode_messages[topic_name]
            self.list.SetItem(self.last_index, 3, self.last_control)
