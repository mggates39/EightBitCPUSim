import wx
from pubsub import pub

from Sap1Emulator.ALU import Alu
from Sap1Emulator.Accumulator import Accumulator
from Sap1Emulator.Bus import Bus
from Sap1Emulator.Clock import Clock
from Sap1Emulator.ControlLogic import ControlLogic
from Sap1Emulator.InstructionRegister import InstructionRegister
from Sap1Emulator.Memory import Memory
from Sap1Emulator.MemoryAddressRegister import MemoryAddressRegister
from Sap1Emulator.OutputRegister import OutputRegister
from Sap1Emulator.ProgramCounter import ProgramCounter
from Sap1Emulator.TempRegister import TempRegister
from Sap1Emulator.StatusRegister import StatusRegister
from Sap1Emulator.History import ExecutionHistory


class CPU(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(675, 700))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "SAP 1 CPU", wx.DefaultPosition, (675, 700))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        self.resetPanel = wx.Panel(self.box)
        self.resetButton = wx.Button(self.box, -1, "Reset")
        panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel_sizer.Add(self.resetButton, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        self.resetPanel.SetSizer(panel_sizer)


        self.bus = Bus(self.box)
        self.clock = Clock(self.box)
        self.pc = ProgramCounter(self.box)
        self.mar = MemoryAddressRegister(self.box)
        self.acc = Accumulator(self.box)
        self.mem = Memory(self.box)
        self.ir = InstructionRegister(self.box)
        self.alu = Alu(self.box)
        self.tmp = TempRegister(self.box)
        self.out = OutputRegister(self.box)
        self.cl = ControlLogic(self.box)
        self.sr = StatusRegister(self.box)
        self.history = ExecutionHistory(self.box)

        self.sizer = wx.GridBagSizer(10, 10)
        self.sizer.Add(self.resetPanel, pos=(0,0), span=(1,5))
        self.sizer.Add(self.clock, pos=(1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mar, pos=(2, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mem, pos=(3, 0), span=(9, 1), flag=wx.EXPAND)
        self.sizer.Add(self.ir, pos=(12, 0), flag=wx.EXPAND)

        self.sizer.Add(self.bus, pos=(1, 1), span=(12, 1), flag=wx.EXPAND)

        self.sizer.Add(self.pc, pos=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.acc, pos=(2, 2), flag=wx.EXPAND)
        self.sizer.Add(self.alu, pos=(3, 2), span=(7, 1), flag=wx.EXPAND)
        self.sizer.Add(self.tmp, pos=(10, 2), flag=wx.EXPAND)
        self.sizer.Add(self.out, pos=(11, 2), flag=wx.EXPAND)
        self.sizer.Add(self.cl, pos=(12, 2), span=(1, 3), flag=wx.EXPAND)

        self.sizer.Add(self.history, pos=(1,3), span=(11,3), flag=wx.EXPAND)

        self.sizer.Add(self.sr, pos=(12,5), flag=wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.SetSizer(nmSizer)

        self.resetButton.Bind(wx.EVT_BUTTON, self.on_click_reset)

    def load_memory(self, memory):
        data = []
        idx = 0
        for mem in memory.get_memory_array():
            data.append( ("0x{0:X}:".format(idx), "{0:08b}".format(mem)) )
            idx += 1

        self.mem.load_data(data)
        pub.sendMessage('CPU.Reset')

    def on_click_reset(self, e):
        pub.sendMessage('CPU.Reset')
