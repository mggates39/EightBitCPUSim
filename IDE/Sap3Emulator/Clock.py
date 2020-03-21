"""
    Clock.py
    ------

    This module contains the CPU Clock management and display.
"""

import wx
from pubsub import pub


class Clock(wx.Panel):
    """
    The Clock class implements a periodic or manual clock tick that drives the CPU
    through the execution of the microcode for each instruction.  This is displayed inside a wxPython Panel
    """

    def __init__(self, parent):
        """
        Create a new Clock Panel

        :param parent: Panel that will contain this Bus Panel
        """
        wx.Panel.__init__(self, parent, size=(300, 150))
        self.parent = parent
        self.index = 0
        self.halted = False
        self.paused = False
        self.resume_timer = False
        self.speed = 100
        self.timer = wx.Timer(self)
        self.box = wx.StaticBox(self, wx.ID_ANY, "Clock", wx.DefaultPosition, (300, 150))
        static_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        button_box = wx.BoxSizer(wx.HORIZONTAL)
        self.start_clock = wx.Button(self.box, -1, "Start")
        self.stop_clock = wx.Button(self.box, -1, "stop")
        self.stop_clock.Enable(False)
        self.single_step = wx.Button(self.box, -1, "Step")
        button_box.Add(self.start_clock, 0, wx.ALL | wx.EXPAND, 2)
        button_box.Add(self.stop_clock, 0, wx.ALL | wx.EXPAND, 2)
        button_box.Add(self.single_step, 0, wx.ALL | wx.EXPAND, 2)

        self.slider = wx.Slider(self.box, value=self.speed, maxValue=1000, minValue=5, size=(240, 20),
                                style=wx.HORIZONTAL)
        self.slider.SetFocus()

        vertical_box.Add(button_box, 1, wx.EXPAND)
        vertical_box.Add(self.slider, 1, wx.ALIGN_LEFT | wx.TOP, 5)

        self.panel = wx.Panel(self.box, size=(40, 75))
        self.halt_indicator = wx.StaticText(self.panel, label="HLT")
        self.pause_indicator = wx.StaticText(self.panel, label="WAIT")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.halt_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(self.pause_indicator, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.panel.SetSizer(vbox)

        horizontal_box.Add(self.panel, 0)
        horizontal_box.Add(vertical_box, 1, wx.EXPAND)

        static_box_sizer.Add(horizontal_box, 1, wx.EXPAND)

        self.SetSizer(static_box_sizer)

        pub.subscribe(self.on_halt, 'CPU.Halt')
        pub.subscribe(self.on_pause, 'CPU.Pause')
        pub.subscribe(self.on_reset, 'CPU.Reset')
        pub.subscribe(self.on_resume, 'CPU.InputResponse')

        self.start_clock.Bind(wx.EVT_BUTTON, self.on_start_clock_click)
        self.stop_clock.Bind(wx.EVT_BUTTON, self.on_stop_clock_click)
        self.single_step.Bind(wx.EVT_BUTTON, self.on_step_clock_click)
        self.Bind(wx.EVT_TIMER, self.on_step_clock_click, self.timer)
        self.Bind(wx.EVT_SCROLL, self.on_scroll)

    def on_reset(self) -> None:
        """
        Process the CPU.Reset signal.

         Reset the clock to the initial state, turn off all indicators and enable or disable the proper buttons.
        """
        self.index = 0
        self.halted = False
        self.paused = False
        self.resume_timer = False
        self.halt_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.pause_indicator.SetForegroundColour((0, 0, 0))  # set text color
        self.start_clock.Enable(True)
        self.stop_clock.Enable(False)
        self.single_step.Enable(True)
        if self.timer.IsRunning():
            self.timer.Stop()

    def on_halt(self) -> None:
        """
        Process the CPU.Halt signal.

        Halts the clock timer if running and set the Halt indicator.
        """
        self.halted = True
        self.halt_indicator.SetForegroundColour((0, 0, 255))  # set text color
        self.start_clock.Enable(False)
        self.stop_clock.Enable(False)
        self.single_step.Enable(False)
        if self.timer.IsRunning():
            self.timer.Stop()

    def on_pause(self) -> None:
        """
        Process the CPU.Pause signal.

        Halts the clock timer if running and set the Halt indicator.
        """
        self.paused = True
        self.resume_timer = False
        self.pause_indicator.SetForegroundColour((0, 0, 255))  # set text color
        if self.timer.IsRunning():
            self.timer.Stop()
            self.resume_timer = True

    def on_resume(self) -> None:
        """
        Process the CPU.Pause signal.

        Halts the clock timer if running and set the Halt indicator.
        """
        self.paused = False
        self.pause_indicator.SetForegroundColour((0, 0, 0))  # set text color
        if self.resume_timer:
            self.on_start_clock_click(None)

        self.resume_timer = False

    def on_start_clock_click(self, e: wx.MouseEvent) -> None:
        """
        Start the timer at the selected speed.  This allows Timer Events to advance the CPU.

        :param e: Mouse Event - Unused
        """
        self.start_clock.Enable(False)
        self.stop_clock.Enable(True)
        self.single_step.Enable(False)
        self.timer.Start(1005 - self.speed)

    def on_stop_clock_click(self, e: wx.MouseEvent) -> None:
        """
        Stops the timer if it is running.  This prevents any Timer Events from advancing the CPU.

        :param e: Mouse Event - Unused
        """
        if self.timer.IsRunning():
            self.timer.Stop()

        self.start_clock.Enable(True)
        self.stop_clock.Enable(False)
        self.single_step.Enable(True)

    def on_step_clock_click(self, e: wx.Event) -> None:
        """
        Fires on every Timer event or click of the Clock Step button.  It sends
        a CPU.Clock signal to all the components in the CPU.  This is the
        driving force of the Emulator.

        :param e: Mouse or Timer Event - Unused
        """
        if not self.halted:
            pub.sendMessage('clock.active', new_active=True)
            pub.sendMessage("CPU.ClearControl")
            pub.sendMessage('CPU.Clock')
            pub.sendMessage('clock.active', new_active=False)

        self.parent.parent.Refresh()

    def on_scroll(self, e: wx.ScrollEvent) -> None:
        """
        Handle the scrolling event generated by the speed slider.  Adjust the delay to speed up
        or slow down the CPU clock.

        :param e: Scroll Event that contains the value of the slider as an integer
        """
        self.speed = e.GetInt()
        if self.timer.IsRunning():
            self.timer.Start(1005 - self.speed)
