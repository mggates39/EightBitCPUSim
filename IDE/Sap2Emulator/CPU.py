import wx
from pubsub import pub

from Sap1Emulator.OutputRegister import OutputRegister
from Sap2Emulator.ALU import Alu
from Sap2Emulator.Accumulator import Accumulator
from Sap2Emulator.Bus import Bus
from Sap2Emulator.Clock import Clock
from Sap2Emulator.ControlLogic import ControlLogic
from Sap2Emulator.History import ExecutionHistory
from Sap2Emulator.InstructionRegister import InstructionRegister
from Sap2Emulator.Memory import Memory
from Sap2Emulator.MemoryAddressRegister import MemoryAddressRegister
from Sap2Emulator.MicroCode import MicroCode
from Sap2Emulator.ProgramCounter import ProgramCounter
from Sap2Emulator.Reset import Reset
from Sap2Emulator.StatusRegister import StatusRegister
from Sap2Emulator.TempRegister import TempRegister


class CPU(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(1024, 800))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "SAP 2 CPU", wx.DefaultPosition, (1024, 800))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)

        self.microcode_engine = MicroCode()
        self.reset = Reset(self.box)
        self.bus = Bus(self.box)
        self.clock = Clock(self.box)
        self.pc = ProgramCounter(self.box)
        self.mar = MemoryAddressRegister(self.box)
        self.a_register = Accumulator(self.box, name="A")
        self.b_register = Accumulator(self.box, name="B")
        self.c_register = Accumulator(self.box, name="C")
        self.mem = Memory(self.box)
        self.alu = Alu(self.box)
        self.tmp = TempRegister(self.box)
        self.out = OutputRegister(self.box)
        self.cl = ControlLogic(self.box)
        self.sr = StatusRegister(self.box)
        self.ir = InstructionRegister(self.box, self.microcode_engine)
        self.history = ExecutionHistory(self.box)

        self.sizer = wx.GridBagSizer(10, 10)

        self.sizer.Add(self.reset, pos=(0, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mar, pos=(1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mem, pos=(2, 0), span=(10, 1), flag=wx.EXPAND)
        self.sizer.Add(self.ir, pos=(12, 0), flag=wx.EXPAND)

        self.sizer.Add(self.clock, pos=(0, 1), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.bus, pos=(1, 1), span=(12, 1), flag=wx.EXPAND)

        self.sizer.Add(self.a_register, pos=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.alu, pos=(2, 2), span=(8, 1), flag=wx.EXPAND)
        self.sizer.Add(self.tmp, pos=(10, 2), flag=wx.EXPAND)
        self.sizer.Add(self.out, pos=(11, 2), flag=wx.EXPAND)
        self.sizer.Add(self.cl, pos=(12, 2), span=(1, 2), flag=wx.EXPAND)

        self.sizer.Add(self.pc, pos=(0, 3), flag=wx.EXPAND)
        self.sizer.Add(self.b_register, pos=(1, 3), flag=wx.EXPAND)
        self.sizer.Add(self.history, pos=(2, 3), span=(10, 2), flag=wx.EXPAND)

        self.sizer.Add(self.sr, pos=(12, 4), flag=wx.EXPAND)
        self.sizer.Add(self.c_register, pos=(1, 4), flag=wx.EXPAND)

        static_box_sizer.Add(self.sizer, 1, wx.EXPAND)
        self.SetSizer(static_box_sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

    def load_memory(self, memory):
        data = []
        idx = 0
        for mem in memory.get_memory_array():
            data.append(("0x{0:04X}:".format(idx), "{0:08b}".format(mem)))
            idx += 1

        self.mem.load_data(data)
        pub.sendMessage('CPU.Reset')
