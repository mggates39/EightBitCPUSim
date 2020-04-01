"""
    ALU.py
    ------

    This module contains the Arithmetic Logic Unit implementation and display.
"""

import wx
from pubsub import pub

from GuiComponents.LedArray import LEDArray
from GuiComponents.LedArray import MODE_HEX


class Alu(wx.Panel):
    """
    The Alu class implements the ALU and manages the display of its values, flags and control signal representations
    inside a wxPython Panel
    """

    def __init__(self, parent):
        """
        Create a new ALU Panel

        :param parent: Panel that will contain this ALU Panel
        """
        wx.Panel.__init__(self, parent, size=(100, 300))
        self.parent = parent
        self.result = 0
        self.buffer = 0
        self.value = 0
        self.a_value = 0
        self.b_value = 0
        self.c_value = 0
        self.d_value = 0
        self.e_value = 0
        self.h_value = 0
        self.l_value = 0
        self.temp_value = 0
        self.auxillary_carry = False
        self.carry = False
        self.zero = False
        self.sign = False
        self.parity = False
        self.subtract = False
        self.logical_and = False
        self.logical_or = False
        self.logical_xor = False
        self.logical_roll_right = False
        self.logical_roll_left = False
        self.through_carry = False
        self.decimal_adjust_accumulator = False

        self.box = wx.StaticBox(self, wx.ID_ANY, "ALU", wx.DefaultPosition, (100, 300))
        self.static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.panel = wx.Panel(self.box, size=(50, 75))
        self.read_indicator = wx.StaticText(self.panel, label="EO")
        self.write_indicator = wx.StaticText(self.panel, label="EI")
        self.add_indicator = wx.StaticText(self.panel, label="ADD")
        self.subtract_indicator = wx.StaticText(self.panel, label="SUB")
        self.complement_indicator = wx.StaticText(self.panel, label="CMA")
        self.logical_and_indicator = wx.StaticText(self.panel, label="LAND")
        self.logical_or_indicator = wx.StaticText(self.panel, label="LOR")
        self.logical_xor_indicator = wx.StaticText(self.panel, label="LXOR")
        self.logical_roll_right_indicator = wx.StaticText(self.panel, label="RAR")
        self.logical_roll_left_indicator = wx.StaticText(self.panel, label="RAL")
        self.use_carry_indicator = wx.StaticText(self.panel, label="USC")
        self.daa_indicator = wx.StaticText(self.panel, label="DAA")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.add_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.subtract_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.complement_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.logical_and_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.logical_or_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.logical_xor_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.logical_roll_right_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.logical_roll_left_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.use_carry_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        vbox.Add(self.daa_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        self.panel.SetSizer(vbox)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.leds = LEDArray(self.box, 8, topic="alu.set_value", mode=MODE_HEX)
        self.carry_flag = wx.StaticText(self.box, label="Carry-Bit: False", style=wx.ALIGN_CENTRE)
        self.zero_flag = wx.StaticText(self.box, label="Zero-Bit: False", style=wx.ALIGN_CENTRE)
        self.minus_flag = wx.StaticText(self.box, label="Sign-Bit: False", style=wx.ALIGN_CENTRE)
        self.parity_flag = wx.StaticText(self.box, label="Parity-Bit: False", style=wx.ALIGN_CENTRE)
        vertical_box.Add(self.leds, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
        vertical_box.Add(self.carry_flag, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vertical_box.Add(self.zero_flag, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vertical_box.Add(self.minus_flag, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        vertical_box.Add(self.parity_flag, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        hbox.Add(vertical_box, 1, wx.EXPAND)
        hbox.Add(self.panel, 0, wx.EXPAND)

        self.static_box_sizer.Add(hbox, 1, wx.EXPAND)

        self.SetSizer(self.static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.on_in, 'CPU.AluIn')
        pub.subscribe(self.on_out, 'CPU.AluOut')

        pub.subscribe(self.on_add, 'CPU.AluAdd')
        pub.subscribe(self.on_subtract, 'CPU.AluSub')

        pub.subscribe(self.on_complement, 'CPU.AluCma')

        pub.subscribe(self.on_decrement, 'CPU.AluDec')
        pub.subscribe(self.on_increment, 'CPU.AluInc')

        pub.subscribe(self.on_and, 'CPU.AluLand')
        pub.subscribe(self.on_or, 'CPU.AluLor')
        pub.subscribe(self.on_xor, 'CPU.AluLxor')

        pub.subscribe(self.on_rar, 'CPU.AluRar')
        pub.subscribe(self.on_ral, 'CPU.AluRal')

        pub.subscribe(self.on_use_carry, 'CPU.AluUseCarry')

        pub.subscribe(self.on_decimal_adjust, 'CPU.AluDaa')

        pub.subscribe(self.on_use_a_value, 'CPU.AluLda')
        pub.subscribe(self.on_use_b_value, 'CPU.AluLdb')
        pub.subscribe(self.on_use_c_value, 'CPU.AluLdc')
        pub.subscribe(self.on_use_d_value, 'CPU.AluLdd')
        pub.subscribe(self.on_use_e_value, 'CPU.AluLde')
        pub.subscribe(self.on_use_h_value, 'CPU.AluLdh')
        pub.subscribe(self.on_use_l_value, 'CPU.AluLdl')

        pub.subscribe(self.on_save_flags, 'CPU.FlagIn')

        pub.subscribe(self.on_get_a_value, 'alu.set_value_AReg')
        pub.subscribe(self.on_get_b_value, 'alu.set_value_BReg')
        pub.subscribe(self.on_get_c_value, 'alu.set_value_CReg')
        pub.subscribe(self.on_get_d_value, 'alu.set_value_DReg')
        pub.subscribe(self.on_get_e_value, 'alu.set_value_EReg')
        pub.subscribe(self.on_get_h_value, 'alu.set_value_HReg')
        pub.subscribe(self.on_get_l_value, 'alu.set_value_LReg')
        pub.subscribe(self.on_temp_value, 'alu.set_value_temp')

    def set_add_display_flag(self):
        """
        Turn on the Addition Control signal display.
        """
        self.add_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_sub_display_flag(self):
        """
        Turn on the Subtraction Control signal display.
        """
        self.subtract_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_complement_display_flag(self):
        """
        Turn on the 2's complement Control signal display.
        """
        self.complement_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_use_carry_display_flag(self):
        """
        Turn on the use carry Control signal display.
        """
        self.use_carry_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_daa_display_flag(self):
        """
        Turn on the use carry Control signal display.
        """
        self.daa_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_in_display_flag(self):
        """
        Turn on the Execution In Control signal display.
        """
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        """
        Turn on the Execution Out Control signal display.
        """
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_and_display_flag(self):
        """
        Turn on the Logical And Control signal display.
        """
        self.logical_and_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_or_display_flag(self):
        """
        Turn on the Logical Or Control signal display.
        """
        self.logical_or_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_xor_display_flag(self):
        """
        Turn on the Logical Xor Control signal display.
        """
        self.logical_xor_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_rar_display_flag(self):
        """
        Turn on the Logical roll right Control signal display.
        """
        self.logical_roll_right_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_ral_display_flag(self):
        """
        Turn on the Logical roll left Control signal display.
        """
        self.logical_roll_left_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        """
        Clear all the display flag indicators.  Usually called from the :meth: `on_clock` message handler.
        """
        self.add_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.subtract_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.complement_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.logical_and_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.logical_or_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.logical_xor_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.logical_roll_right_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.logical_roll_left_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.use_carry_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.daa_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        """
        Receive the CPU Clock signal
        """
        self.subtract = False
        self.logical_and = False
        self.logical_or = False
        self.logical_xor = False
        self.logical_roll_right = False
        self.logical_roll_left = False
        self.through_carry = False
        self.decimal_adjust_accumulator = False
        self.clear_display_flags()

    def on_reset(self):
        """
        Receive the CPU Reset control signal
        """
        self.result = 0
        self.buffer = 0
        self.value = 0
        self.a_value = 0
        self.b_value = 0
        self.c_value = 0
        self.d_value = 0
        self.e_value = 0
        self.h_value = 0
        self.l_value = 0
        self.temp_value = 0
        self.auxillary_carry = False
        self.carry = False
        self.zero = False
        self.sign = False
        self.parity = False
        self.subtract = False
        self.logical_and = False
        self.logical_or = False
        self.logical_xor = False
        self.logical_roll_right = False
        self.logical_roll_left = False
        self.through_carry = False
        self.decimal_adjust_accumulator = False
        self.clear_display_flags()
        pub.sendMessage('alu.set_value', new_value=self.result)

    def on_get_a_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.a_value = new_value

    def on_use_a_value(self) -> None:
        self.value = self.a_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_b_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.b_value = new_value

    def on_use_b_value(self) -> None:
        self.value = self.b_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_c_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.c_value = new_value

    def on_use_c_value(self) -> None:
        self.value = self.c_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_d_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.d_value = new_value

    def on_use_d_value(self) -> None:
        self.value = self.d_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_e_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.e_value = new_value

    def on_use_e_value(self) -> None:
        self.value = self.e_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_h_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.h_value = new_value

    def on_use_h_value(self) -> None:
        self.value = self.h_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_get_l_value(self, new_value: int) -> None:
        """
        Receive a new value from the Accumulator (a) register.

        :param new_value: New value from the A Register
        """
        self.l_value = new_value

    def on_use_l_value(self) -> None:
        self.value = self.l_value
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_temp_value(self, new_value: int) -> None:
        """
        Receive a new value from the temp (b) register.

        :param new_value: New value from the A Register
        """
        self.temp_value = new_value

    def on_add(self):
        """
        Receive the add control message and do_math.
        """
        self.set_add_display_flag()
        self.subtract = False
        self.do_math()

    def on_subtract(self):
        """
        Receive the subtract control message and enable subtraction in do_math.
        """
        self.set_sub_display_flag()
        self.subtract = True
        self.do_math()

    def on_increment(self):
        self.set_add_display_flag()
        self.temp_value = 1
        self.subtract = False
        self.do_math()

    def on_decrement(self):
        self.set_sub_display_flag()
        self.temp_value = 1
        self.subtract = True
        self.do_math()

    def on_complement(self):
        self.set_complement_display_flag()
        self.value = ~self.value
        self.temp_value = 0
        self.subtract = False
        self.do_math()

    def on_and(self):
        self.set_and_display_flag()
        self.logical_and = True
        self.do_logic()

    def on_or(self):
        self.set_or_display_flag()
        self.logical_or = True
        self.do_logic()

    def on_xor(self):
        self.set_xor_display_flag()
        self.logical_xor = True
        self.do_logic()

    def on_rar(self):
        self.set_rar_display_flag()
        self.logical_roll_right = True
        self.logical_roll_left = False
        self.do_logic()

    def on_ral(self):
        self.set_ral_display_flag()
        self.logical_roll_right = False
        self.logical_roll_left = True
        self.do_logic()

    def on_use_carry(self):
        self.set_use_carry_display_flag()
        self.through_carry = True

    def on_decimal_adjust(self):
        self.set_daa_display_flag()
        self.decimal_adjust_accumulator = True
        # @todo Descimal Adjust Accumulater requires a working Aux Carry

    def determine_status_flags(self, new_value):

        if new_value == 0:
            self.zero = True
        else:
            self.zero = False

        if new_value & 0x80 == 0x80:
            self.sign = True
        else:
            self.sign = False

        number_bits = 0
        for i in range(0, 8):
            bit = 2 ** i
            if new_value & bit == bit:
                number_bits += 1

        if number_bits % 2 == 0:
            self.parity = True
        else:
            self.parity = False

    def perform_add(self, a, b):
        if self.through_carry and self.carry:
            used_carry = 1
        else:
            used_carry = 0

        value = a + b + used_carry
        return_value = value & 0xFF
        if value & 0x100 == 0x100:
            self.carry = True
        else:
            self.carry = False
        return return_value

    def perform_sub(self, minuend, subtrahend):
        subt_ones = (~subtrahend) & 0xFF

        if self.through_carry and self.carry:
            used_carry = 0
        else:
            used_carry = 1

        value = minuend + subt_ones + used_carry
        return_value = value & 0xFF
        if value & 0x100 == 0x100:
            self.carry = False
        else:
            self.carry = True
        return return_value

    def do_math(self):
        """
        Do the math calculation.  Addition by default, but subtraction if
        the subtract flag is set.
        Then update the carry and zero flag values accordingly
        """
        if self.subtract:
            self.result = self.perform_sub(self.value, self.temp_value)
        else:
            self.result = self.perform_add(self.value, self.temp_value)

        self.determine_status_flags(self.result)

        self.set_carry_label(self.carry)
        self.set_zero_label(self.zero)
        self.set_sign_label(self.sign)
        self.set_parity_label(self.parity)
        pub.sendMessage('alu.set_value', new_value=self.result)

    def do_logic(self):
        """
        Do the math calculation.  Addition by default, but subtraction if
        the subtract flag is set.
        Then update the carry and zero flag values accordingly
        """
        is_roll = False
        if self.logical_roll_left:
            is_roll = True
            new_carry = self.value & 0x80 == 0x80
            if self.through_carry:
                if self.carry:
                    new_zero_bit = 0x01
                else:
                    new_zero_bit = 0x00
            else:
                if new_carry:
                    new_zero_bit = 0x01
                else:
                    new_zero_bit = 0x00

            self.result = (self.value << 1 | new_zero_bit) & 0xFF
            self.carry = new_carry

        if self.logical_roll_right:
            is_roll = True
            new_carry = self.value & 0x01 == 0x01
            if self.through_carry:
                if self.carry:
                    new_bit_seven = 0x80
                else:
                    new_bit_seven = 0x00
            else:
                if new_carry:
                    new_bit_seven = 0x80
                else:
                    new_bit_seven = 0x00

            self.result = (self.value >> 1 | new_bit_seven) & 0xFF
            self.carry = new_carry

        if self.logical_and:
            self.result = self.value & self.temp_value
            self.carry = False

        if self.logical_or:
            self.result = self.value | self.temp_value
            self.carry = False

        if self.logical_xor:
            self.result = self.value ^ self.temp_value
            self.carry = False

        if not is_roll:
            self.determine_status_flags(self.result)

        self.set_carry_label(self.carry)
        self.set_zero_label(self.zero)
        self.set_sign_label(self.sign)
        self.set_parity_label(self.parity)
        pub.sendMessage('alu.set_value', new_value=self.result)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in(self):
        self.value = self.buffer
        self.set_in_display_flag()
        pub.sendMessage('alu.set_value', new_value=self.value)

    def on_out(self):
        """
        Send message to the bus that there is a new value to read.
        """
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=self.result)

    def on_save_flags(self):
        """
        Send out the current carry and zero status flags.
        """
        pub.sendMessage("alu.FlagValues", new_carry=self.carry, new_zero=self.zero, new_sign=self.sign,
                        new_parity=self.parity, new_auxillary_carry=self.auxillary_carry)

    def set_carry_label(self, new_label: bool) -> None:
        """
        Set the label to be displayed for the Carry Flag.

        :param new_label: New state of the carry flag
        """
        self.carry_flag.SetLabel("Carry-Bit: {}".format(new_label))
        self.static_box_sizer.Layout()

    def set_zero_label(self, new_label: bool) -> None:
        """
        Set the label to be displayed for the Zero Flag.

        :param new_label: New state of the zero flag
        """
        self.zero_flag.SetLabel("Zero-Bit: {}".format(new_label))
        self.static_box_sizer.Layout()

    def set_sign_label(self, new_label: bool) -> None:
        """
        Set the label to be displayed for the Minus Flag.

        :param new_label: New state of the zero flag
        """
        self.minus_flag.SetLabel("Sign-Bit: {}".format(new_label))
        self.static_box_sizer.Layout()

    def set_parity_label(self, new_label: bool) -> None:
        """
        Set the label to be displayed for the Minus Flag.

        :param new_label: New state of the zero flag
        """
        self.parity_flag.SetLabel("parity-Bit: {}".format(new_label))
        self.static_box_sizer.Layout()
