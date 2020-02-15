import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray


class InstructionRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.value = 0
        self.buffer = 0
        self.carry_flag = 0
        self.zero_flag = 0
        self.box = wx.StaticBox(self, wx.ID_ANY, "Instruction Register", wx.DefaultPosition, (100, 75))
        nmSizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        vertical_box = wx.BoxSizer(wx.HORIZONTAL)

        self.instruction = LEDArray(self.box, 4, topic="ip.set_instruction")
        self.data = LEDArray(self.box, 4, topic="ip.set_data")

        vertical_box.Add(self.instruction, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
        vertical_box.Add(self.data, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)

        nmSizer.Add(vertical_box, 1, wx.EXPAND)

        self.SetSizer(nmSizer)

        self.operators = {0: {"operator": "NOP", "opcode": 0, "operand": None,
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.RingReset']]},
                          1: {"operator": "LDA <A>", "opcode": 1, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.AccIn'],
                                            ['CPU.RingReset']]},
                          2: {"operator": "ADD <A>", "opcode": 2, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.TempIn'],
                                            ['CPU.FlagIn', 'CPU.AluOut', 'CPU.AccpIn'],
                                            ['CPU.RingReset']]},
                          3: {"operator": "SUB <A>", "opcode": 3, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.TempIn'],
                                            ['CPU.AluSub', 'CPU.FlagIn', 'CPU.AluOut', 'CPU.AccpIn'],
                                            ['CPU.RingReset']]},
                          4: {"operator": "STA <A>", "opcode": 4, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.MarIn'],
                                            ['CPU.AccOut', 'CPU.MemIn'],
                                            ['CPU.RingReset']]},
                          5: {"operator": "LDI", "opcode": 5, "operand": "N",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.AccIn'],
                                            ['CPU.RingReset']]},
                          6: {"operator": "JMP <A>", "opcode": 6, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.IrOut', 'CPU.PcJump'],
                                            ['CPU.RingReset']]},
                          7: {"operator": "JC <A>", "opcode": 7, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.RingReset']]},
                          8: {"operator": "JZ <A>", "opcode": 8, "operand": "M",
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.RingReset']]},
                          9: {"operator": "NOP", "opcode": 9, "operand": None,
                              "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                            ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                            ['CPU.RingReset']]},
                          10: {"operator": "NOP", "opcode": 10, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.RingReset']]},
                          11: {"operator": "NOP", "opcode": 11, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.RingReset']]},
                          12: {"operator": "NOP", "opcode": 12, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.RingReset']]},
                          13: {"operator": "NOP", "opcode": 13, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.RingReset']]},
                          14: {"operator": "OUT", "opcode": 14, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.AccOut', 'CPU.OutputWrite'],
                                             ['CPU.RingReset']]},
                          15: {"operator": "HLT", "opcode": 15, "operand": None,
                               "microcode": [['CPU.PcOut', 'CPU.MarIn'],
                                             ['CPU.MemOut', 'CPU.IrIn', 'CPU.PcInc'],
                                             ['CPU.Halt'],
                                             ['CPU.RingReset']]}
                          }
        self.on_reset()

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.IrIn')
        pub.subscribe(self.on_out, 'CPU.IrOut')
        pub.subscribe(self.on_read_flags, 'CPU.FlagValues')

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
        self.on_clock()
        op_code = int((self.value >> 4) & 15)
        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label="NOP")
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        op_code = int((self.value >> 4) & 15)
        operator = self.operators[op_code]["operator"]
        pub.sendMessage('ip.set_instruction', new_value=op_code)
        pub.sendMessage('ip.set_instruction_label', new_label=operator)
        pub.sendMessage('ip.set_data', new_value=(self.value & 15))

    def on_out(self):
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=(self.value & 15))

    def on_read_flags(self, carry, zero):
        self.carry_flag = carry
        self.zero_flag = zero