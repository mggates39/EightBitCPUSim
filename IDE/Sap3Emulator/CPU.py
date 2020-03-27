import wx
from pubsub import pub

from Sap3Emulator.ALU import Alu
from Sap3Emulator.Accumulator import Accumulator
from Sap3Emulator.Bus import Bus
from Sap3Emulator.Clock import Clock
from Sap3Emulator.ControlLogic import ControlLogic
from Sap3Emulator.History import ExecutionHistory
from Sap3Emulator.InputRegister import InputRegister
from Sap3Emulator.InstructionRegister import InstructionRegister
from Sap3Emulator.Memory import Memory
from Sap3Emulator.MemoryAddressRegister import MemoryAddressRegister
from Sap3Emulator.MicroCode import MicroCode
from Sap3Emulator.OutputRegister import OutputRegister
from Sap3Emulator.ProgramCounter import ProgramCounter
from Sap3Emulator.Reset import Reset
from Sap3Emulator.StackRegister import StackRegister
from Sap3Emulator.StatusRegister import StatusRegister
from Sap3Emulator.TempRegister import TempRegister


class CPU(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(1500, 900))
        self.parent = parent
        self.box = wx.StaticBox(self, wx.ID_ANY, "SAP 3 CPU", wx.DefaultPosition, (1024, 800))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)

        self.microcode_engine = MicroCode()
        self.reset = Reset(self)
        self.bus = Bus(self)
        self.clock = Clock(self)
        self.pc = ProgramCounter(self)
        self.sp = StackRegister(self)
        self.mar = MemoryAddressRegister(self)
        self.a_register = Accumulator(self, name="A")
        self.b_register = Accumulator(self, name="B")
        self.c_register = Accumulator(self, name="C")
        self.d_register = Accumulator(self, name="D")
        self.e_register = Accumulator(self, name="E")
        self.h_register = Accumulator(self, name="H")
        self.l_register = Accumulator(self, name="L")
        self.mem = Memory(self)
        self.alu = Alu(self)
        self.tmp = TempRegister(self)
        self.out = OutputRegister(self)
        self.input = InputRegister(self)
        self.cl = ControlLogic(self)
        self.sr = StatusRegister(self)
        self.ir = InstructionRegister(self, self.microcode_engine)
        self.history = ExecutionHistory(self)

        self.sizer = wx.GridBagSizer(7, 7)
        self.sizer.Add(self.mar, pos=(0, 0), flag=wx.EXPAND)
        self.sizer.Add(self.bus, pos=(0, 1), span=(6, 1), flag=wx.EXPAND)
        self.sizer.Add(self.pc, pos=(0, 2), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.sp, pos=(0, 4), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.history, pos=(0, 6), span=(4, 1), flag=wx.EXPAND)

        self.sizer.Add(self.mem, pos=(1, 0), span=(5, 1), flag=wx.EXPAND)
        self.sizer.Add(self.a_register, pos=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.sr, pos=(1, 3), flag=wx.EXPAND)
        self.sizer.Add(self.b_register, pos=(1, 4), flag=wx.EXPAND)
        self.sizer.Add(self.c_register, pos=(1, 5), flag=wx.EXPAND)
        self.sizer.Add(self.d_register, pos=(2, 2), flag=wx.EXPAND)
        self.sizer.Add(self.e_register, pos=(2, 3), flag=wx.EXPAND)
        self.sizer.Add(self.h_register, pos=(2, 4), flag=wx.EXPAND)
        self.sizer.Add(self.l_register, pos=(2, 5), flag=wx.EXPAND)
        self.sizer.Add(self.ir, pos=(3, 2), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.alu, pos=(3, 4), span=(3, 2), flag=wx.EXPAND)
        self.sizer.Add(self.out, pos=(4, 2), flag=wx.EXPAND)
        self.sizer.Add(self.tmp, pos=(4, 3), flag=wx.EXPAND)
        self.sizer.Add(self.input, pos=(4, 6), span=(2, 1), flag=wx.EXPAND)

        self.sizer.Add(self.reset, pos=(5, 2), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.clock, pos=(6, 0), span=(1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.cl, pos=(6, 2), span=(1, 5), flag=wx.EXPAND)

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
