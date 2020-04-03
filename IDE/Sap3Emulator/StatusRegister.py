import wx
from pubsub import pub

from GuiComponents.Led import LED

SIGN_BIT = 0x80
ZERO_BIT = 0x40
AUX_CARRY_BIT = 0x10
PARITY_BIT = 0x04
CARRY_BIT = 0x01


class StatusRegister(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(100, 75))
        self.parent = parent
        self.carry = False
        self.zero = False
        self.sign = False
        self.parity = False
        self.auxillary_carry = False
        self.buffer = 0
        light_color = '#36ff27'
        dark_color = '#077100'
        self.box = wx.StaticBox(self, wx.ID_ANY, "Status Register", wx.DefaultPosition, (100, 75))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        carry_box = wx.BoxSizer(wx.VERTICAL)
        self.carry_flag = wx.StaticText(self, label="CY", style=wx.ALIGN_CENTER)
        self.carry_led = LED(self, light_color, dark_color)
        carry_box.Add(self.carry_flag, 0, wx.TOP | wx.ALIGN_CENTER, 12)
        carry_box.Add(self.carry_led, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        auxillary_carry_box = wx.BoxSizer(wx.VERTICAL)
        self.auxillary_carry_flag = wx.StaticText(self, label="AC", style=wx.ALIGN_CENTER)
        self.auxillary_carry_led = LED(self, light_color, dark_color)
        auxillary_carry_box.Add(self.auxillary_carry_flag, 0, wx.TOP | wx.ALIGN_CENTER, 12)
        auxillary_carry_box.Add(self.auxillary_carry_led, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        zero_box = wx.BoxSizer(wx.VERTICAL)
        self.zero_flag = wx.StaticText(self, label="Z", style=wx.ALIGN_CENTER)
        self.zero_led = LED(self, light_color, dark_color)
        zero_box.Add(self.zero_flag, 0, wx.TOP | wx.ALIGN_CENTER, 12)
        zero_box.Add(self.zero_led, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        sign_box = wx.BoxSizer(wx.VERTICAL)
        self.sign_flag = wx.StaticText(self, label="S", style=wx.ALIGN_CENTER)
        self.sign_led = LED(self, light_color, dark_color)
        sign_box.Add(self.sign_flag, 0, wx.TOP | wx.ALIGN_CENTER, 12)
        sign_box.Add(self.sign_led, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        parity_box = wx.BoxSizer(wx.VERTICAL)
        self.parity_flag = wx.StaticText(self, label="P", style=wx.ALIGN_CENTER)
        self.parity_led = LED(self, light_color, dark_color)
        parity_box.Add(self.parity_flag, 0, wx.TOP | wx.ALIGN_CENTER, 12)
        parity_box.Add(self.parity_led, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        horizontal_box.Add(sign_box, 1, wx.ALIGN_CENTER)
        horizontal_box.Add(zero_box, 1, wx.ALIGN_CENTER)
        horizontal_box.Add(auxillary_carry_box, 1, wx.ALIGN_CENTER)
        horizontal_box.Add(parity_box, 1, wx.ALIGN_CENTER)
        horizontal_box.Add(carry_box, 1, wx.ALIGN_CENTER)

        self.panel = wx.Panel(self.box, size=(30, 75))
        self.read_indicator = wx.StaticText(self.panel, label="FO")
        self.write_indicator = wx.StaticText(self.panel, label="FI")
        self.set_carry_indicator = wx.StaticText(self.panel, label="SC")
        self.complement_carry_indicator = wx.StaticText(self.panel, label="CC")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.write_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        vbox.Add(self.read_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        vbox.Add(self.set_carry_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        vbox.Add(self.complement_carry_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        self.panel.SetSizer(vbox)
        horizontal_box.Add(self.panel, 0, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_clock, 'CPU.Clock')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_bus_change, 'CPU.BusChanged')
        pub.subscribe(self.set_in_display_flag, "CPU.FlagIn")
        pub.subscribe(self.on_set_carry, "CPU.SetCarry")
        pub.subscribe(self.on_invert_carry, "CPU.CompCarry")
        pub.subscribe(self.on_in_psw, "CPU.PswIn")
        pub.subscribe(self.on_out_psw, "CPU.PswOut")
        pub.subscribe(self.on_set_flags, "alu.FlagValues")


    def set_in_display_flag(self):
        self.write_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_out_display_flag(self):
        self.read_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_carry_display_flag(self):
        self.set_carry_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def set_comp_display_flag(self):
        self.complement_carry_indicator.SetForegroundColour((0, 0, 255))  # set text color

    def clear_display_flags(self):
        self.write_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.read_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.set_carry_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.complement_carry_indicator.SetForegroundColour((0, 0, 0))  # set text color

    def on_clock(self):
        self.clear_display_flags()

    def on_reset(self):
        self.carry = False
        self.zero = False
        self.sign = False
        self.parity = False
        self.auxillary_carry = False
        self.buffer = 0
        self.clear_display_flags()
        self.display_flags()

    def on_set_carry(self):
        self.set_carry_display_flag()
        self.carry = True
        self.display_flags()

    def on_invert_carry(self):
        self.set_comp_display_flag()
        self.carry = not self.carry
        self.display_flags()

    def encode_psw(self):
        psw = 0x02
        if self.sign:
            psw |= SIGN_BIT
        if self.zero:
            psw |= ZERO_BIT
        if self.auxillary_carry:
            psw |= AUX_CARRY_BIT
        if self.parity:
            psw |= PARITY_BIT
        if self.carry:
            psw |= CARRY_BIT

        return psw

    def decode_psw(self, psw):
        if psw & SIGN_BIT == SIGN_BIT:
            self.sign = True
        else:
            self.sign = False

        if psw & ZERO_BIT == ZERO_BIT:
            self.zero = True
        else:
            self.zero = False

        if psw & AUX_CARRY_BIT == AUX_CARRY_BIT:
            self.auxillary_carry = True
        else:
            self.auxillary_carry = False

        if psw & PARITY_BIT == PARITY_BIT:
            self.parity = True
        else:
            self.parity = False

        if psw & CARRY_BIT == CARRY_BIT:
            self.carry = True
        else:
            self.carry = False

    def on_set_flags(self, new_carry, new_zero, new_sign, new_parity, new_auxillary_carry):
        self.set_in_display_flag()
        self.auxillary_carry = new_auxillary_carry
        self.carry = new_carry
        self.zero = new_zero
        self.sign = new_sign
        self.parity = new_parity
        self.display_flags()

    def display_flags(self):
        self.auxillary_carry_led.light(self.auxillary_carry)
        self.carry_led.light(self.carry)
        self.zero_led.light(self.zero)
        self.sign_led.light(self.sign)
        self.parity_led.light(self.parity)

    def on_bus_change(self, new_value):
        self.buffer = new_value

    def on_in_psw(self):
        self.set_in_display_flag()
        self.decode_psw(self.buffer)
        self.display_flags()
        pub.sendMessage("alu.FlagValues", new_carry=self.carry, new_zero=self.zero, new_sign=self.sign,
                        new_parity=self.parity, new_auxillary_carry=self.auxillary_carry)

    def on_out_psw(self):
        psw = self.encode_psw()
        self.set_out_display_flag()
        pub.sendMessage('CPU.ChangeBus', new_value=psw)
