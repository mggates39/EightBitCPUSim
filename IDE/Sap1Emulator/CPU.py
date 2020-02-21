import wx
from pubsub import pub

from Sap1Emulator.ALU import Alu
from Sap1Emulator.Accumulator import Accumulator
from Sap1Emulator.Bus import Bus
from Sap1Emulator.Clock import Clock
from Sap1Emulator.ControlLogic import ControlLogic
from Sap1Emulator.History import ExecutionHistory
from Sap1Emulator.InstructionRegister import InstructionRegister
from Sap1Emulator.Memory import Memory
from Sap1Emulator.MemoryAddressRegister import MemoryAddressRegister
from Sap1Emulator.MicroCode import MicroCode
from Sap1Emulator.OutputRegister import OutputRegister
from Sap1Emulator.ProgramCounter import ProgramCounter
from Sap1Emulator.Reset import Reset
from Sap1Emulator.StatusRegister import StatusRegister
from Sap1Emulator.TempRegister import TempRegister


class CPU(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(1024, 800))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "SAP 1 CPU", wx.DefaultPosition, (1024, 800))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)

        self.microcode_engine = MicroCode()
        self.reset = Reset(self.box)
        self.bus = Bus(self.box)
        self.clock = Clock(self.box)
        self.pc = ProgramCounter(self.box)
        self.mar = MemoryAddressRegister(self.box)
        self.acc = Accumulator(self.box,name="A")
        self.mem = Memory(self.box)
        self.alu = Alu(self.box)
        self.tmp = TempRegister(self.box)
        self.out = OutputRegister(self.box)
        self.cl = ControlLogic(self.box)
        self.sr = StatusRegister(self.box)
        self.ir = InstructionRegister(self.box, self.microcode_engine)
        self.history = ExecutionHistory(self.box)

        self.sizer = wx.GridBagSizer(10, 10)

        self.sizer.Add(self.reset, pos=(0, 0), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.mar, pos=(1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mem, pos=(2, 0), span=(10, 1), flag=wx.EXPAND)
        self.sizer.Add(self.ir, pos=(12, 0), flag=wx.EXPAND)

        self.sizer.Add(self.bus, pos=(1, 1), span=(12, 1), flag=wx.EXPAND)

        self.sizer.Add(self.clock, pos=(0, 2), span=(1, 4), flag=wx.EXPAND)
        self.sizer.Add(self.pc, pos=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.acc, pos=(2, 2), flag=wx.EXPAND)
        self.sizer.Add(self.alu, pos=(3, 2), span=(7, 1), flag=wx.EXPAND)
        self.sizer.Add(self.tmp, pos=(10, 2), flag=wx.EXPAND)
        self.sizer.Add(self.out, pos=(11, 2), flag=wx.EXPAND)
        self.sizer.Add(self.cl, pos=(12, 2), span=(1, 3), flag=wx.EXPAND)

        self.sizer.Add(self.history, pos=(1, 3), span=(11, 3), flag=wx.EXPAND)

        self.sizer.Add(self.sr, pos=(12, 5), flag=wx.EXPAND)

        static_box_sizer.Add(self.sizer, 1, wx.EXPAND)
        self.SetAutoLayout(1)
        self.SetSizer(static_box_sizer)
        self.sizer.Fit(self)

    def load_memory(self, memory):
        data = []
        idx = 0
        for mem in memory.get_memory_array():
            data.append(("0x{0:X}:".format(idx), "{0:08b}".format(mem)))
            idx += 1

        self.mem.load_data(data)
        pub.sendMessage('CPU.Reset')
