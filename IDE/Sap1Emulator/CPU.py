import wx

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


class CPU(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(675, 700))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "SAP 1 CPU", wx.DefaultPosition, (675, 700))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

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

        self.sizer = wx.GridBagSizer(10, 10)
        self.sizer.Add(self.clock, pos=(0, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mar, pos=(1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.mem, pos=(2, 0), span=(3, 1), flag=wx.EXPAND)
        self.sizer.Add(self.ir, pos=(5, 0), flag=wx.EXPAND)

        self.sizer.Add(self.bus, pos=(0, 1), span=(6, 1), flag=wx.EXPAND)

        self.sizer.Add(self.pc, pos=(0, 2), flag=wx.EXPAND)
        self.sizer.Add(self.acc, pos=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.alu, pos=(2, 2), flag=wx.EXPAND)
        self.sizer.Add(self.tmp, pos=(3, 2), flag=wx.EXPAND)
        self.sizer.Add(self.out, pos=(4, 2), flag=wx.EXPAND)
        self.sizer.Add(self.cl, pos=(5, 2), flag=wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.SetSizer(nmSizer)
