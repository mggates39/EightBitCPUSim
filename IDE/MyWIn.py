import os

import wx
import wx.stc

from Sap1Assembler.Assembler import Assembler
from Sap1Assembler.Parser import is_label
from Sap1Assembler.Parser import make_label
from Sap1Assembler.Parser import make_target

# Define the tab content as classes:
class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.control = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_RICH)
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the third tab", (20,20))



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.directory_name = ''
        self.filename = ''
        self.color_database = wx.ColourDatabase()
        self.labels = []

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200, -1))
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()  # A Status bar in the bottom of the window

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Create the tab windows
        self.tab1 = TabOne(nb)
        self.tab2 = TabTwo(nb)
        self.tab3 = TabThree(nb)

        # Add the windows to tabs and name them.
        nb.AddPage(self.tab1, "Source")
        nb.AddPage(self.tab2, "Listing")
        nb.AddPage(self.tab3, "Execution")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        # Setting up the file menu.
        file_menu = wx.Menu()
        menu_open = file_menu.Append(wx.ID_OPEN, "&Open", " Open a file to edit")
        menu_assemble = file_menu.Append(wx.ID_ANY, "&Assemble", " Assemble text in editor")
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # Setting up the help menu.
        help_menu = wx.Menu()
        menu_about = help_menu.Append(wx.ID_ABOUT, "&About", " Information about this program")

        # Creating the menu_bar.
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")  # Adding the "file_menu" to the MenuBar
        menu_bar.Append(help_menu, "&Help")  # Adding the "help_menu" to the MenuBar
        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_assemble, menu_assemble)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_TEXT, self.highlight_code, self.tab1.control)

        self.Show()

    def on_about(self, e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A sample editor \n in wxPython", "About Sample Editor",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.

    def on_exit(self, e):
        self.Close(True)  # Close the frame.

    def on_open(self, e):
        """ Open a file"""

        dlg = wx.FileDialog(self, "Choose a file", self.directory_name, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.directory_name = dlg.GetDirectory()
            f = open(os.path.join(self.directory_name, self.filename), 'r')
            self.tab1.control.SetValue(f.read())
            f.close()
            self.highlight_code(e)
        dlg.Destroy()

    def on_assemble(self, e):
        a = Assembler()
        lines = self.tab1.control.GetValue()
        text = lines.split("\n")
        listing = a.assemble(text)
        self.tab2.control.Clear()
        for line in listing:
            self.tab2.control.AppendText(line)


    def is_valid_label(self, label):
        found = False
        for x in self.labels:
            if x == label:
                found = True
                break
        return found

    def highlight_code(self, e):
        self.labels = []
        font = self.tab1.control.GetFont()
        comment_attr = wx.TextAttr(self.color_database.Find("LIGHT GREY"), wx.WHITE, font=font)
        label_attr = wx.TextAttr(self.color_database.Find("NAVY"), wx.WHITE, font=font)
        error_attr = wx.TextAttr(wx.WHITE, wx.RED, font=font)
        directive_attr = wx.TextAttr(self.color_database.Find("GOLD"), wx.WHITE, font=font)

        operator_font = self.tab1.control.GetFont()
        operator_font.SetWeight(wx.FONTWEIGHT_BOLD)
        operator_attr = wx.TextAttr(wx.BLACK, wx.WHITE, font=operator_font)

        max_line = self.tab1.control.GetNumberOfLines()
        start_of_line = 0

        for i in range(0, max_line):
            line = self.tab1.control.GetLineText(i)
            if line.startswith('#') or line.startswith(';'):
                continue
            else:
                fields = line.split()
                if len(fields) > 0:
                    if fields[0].endswith(':'):
                        label = make_label(fields[0])
                        self.labels.append(label)

        for i in range(0, max_line):
            line = self.tab1.control.GetLineText(i)
            length = self.tab1.control.GetLineLength(i)
            if line.startswith('#') or line.startswith(';'):
                self.tab1.control.SetStyle(start_of_line, (start_of_line + length), comment_attr)
            else:
                fields = line.split()
                if len(fields) > 0:
                    if fields[0].startswith('.'):
                        self.tab1.control.SetStyle(start_of_line, (start_of_line + (len(fields[0]) + 1)), directive_attr)
                    elif fields[0].endswith(':'):
                        self.tab1.control.SetStyle(start_of_line, (start_of_line + (len(fields[0]))), label_attr)
                        if len(fields) > 1:
                            if fields[1].startswith('.'):
                                self.tab1.control.SetStyle((start_of_line + len(fields[0]) + 1),
                                                      (start_of_line + (len(fields[0]) + 1) + (len(fields[1]) + 1)),
                                                      directive_attr)
                            else:
                                self.tab1.control.SetStyle((start_of_line + len(fields[0]) + 1),
                                                      (start_of_line + (len(fields[0]) + 1) + (len(fields[1]) + 1)),
                                                      operator_attr)
                                if len(fields) == 3:
                                    target = make_target(fields[2])
                                    if is_label(fields[2]):
                                        if self.is_valid_label(target):
                                            self.tab1.control.SetStyle((start_of_line + len(fields[0]) + len(fields[1]) + 3),
                                                                  (start_of_line + len(fields[0]) + len(
                                                                      fields[1]) + 3 + len(target)),
                                                                  label_attr)
                                        else:
                                            self.tab1.control.SetStyle((start_of_line + len(fields[0]) + len(fields[1]) + 3),
                                                                  (start_of_line + len(fields[0]) + len(
                                                                      fields[1]) + 3 + len(target)),
                                                                  error_attr)

                    else:
                        self.tab1.control.SetStyle((start_of_line + 1),
                                              (start_of_line + 1 + (len(fields[0]) + 1)),
                                              operator_attr)
                        if len(fields) == 2:
                            target = make_target(fields[1])
                            if is_label(fields[1]):
                                if self.is_valid_label(target):
                                    self.tab1.control.SetStyle((start_of_line + len(fields[0]) + 4),
                                                          (start_of_line + len(fields[0]) + 4 + len(target)),
                                                          label_attr)
                                else:
                                    self.tab1.control.SetStyle((start_of_line + len(fields[0]) + 4),
                                                          (start_of_line + len(fields[0]) + 4 + len(target)),
                                                          error_attr)

            start_of_line += length + 1


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, "Sample editor")
    app.MainLoop()
