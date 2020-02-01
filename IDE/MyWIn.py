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
        self.control = wx.TextCtrl(self, style=wx.TE_PROCESS_TAB | wx.TE_RICH | wx.TE_MULTILINE)

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
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.reset_listing()

    def reset_listing(self):
        self.control.Clear()
        self.control.AppendText("\n\n\tAssemble Source to see listing!")


class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.reset_memory()

    def reset_memory(self):
        self.control.Clear()
        self.control.AppendText("\n\n\tAssemble Source to see memory!")


class TabFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "This is the fourth tab", (20, 20))


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.directory_name = ''
        self.filename = 'untitled'
        self.base_title = title
        self.color_database = wx.ColourDatabase()
        self.symbol_table = []

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(400, 400))
        self.CreateStatusBar()  # A Status bar in the bottom of the window

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        self.nb = wx.Notebook(p)

        # Create the tab windows
        self.tab1 = TabOne(self.nb)
        self.tab2 = TabTwo(self.nb)
        self.tab3 = TabThree(self.nb)
        self.tab4 = TabFour(self.nb)

        # Add the windows to tabs and name them.
        self.nb.AddPage(self.tab1, "Source")
        self.nb.AddPage(self.tab2, "Listing")
        self.nb.AddPage(self.tab3, "Memory")
        self.nb.AddPage(self.tab4, "Execution")

        # Set notebook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        # Setting up the file menu.
        file_menu = wx.Menu()
        menu_new = file_menu.Append(wx.ID_NEW, "&New", " Create a new edit window")
        menu_open = file_menu.Append(wx.ID_OPEN, "&Open", " Open a file to edit")
        menu_save = file_menu.Append(wx.ID_SAVE, "&Save", " Save the file")
        menu_save_as = file_menu.Append(wx.ID_SAVEAS, "Save As", " Save the file with a new name")
        file_menu.AppendSeparator()
        menu_assemble = file_menu.Append(wx.ID_ANY, "Assemble", " Assemble text in editor")
        file_menu.AppendSeparator()
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
        self.Bind(wx.EVT_MENU, self.on_new, menu_new)
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_save, menu_save)
        self.Bind(wx.EVT_MENU, self.on_save_as, menu_save_as)
        self.Bind(wx.EVT_MENU, self.on_assemble, menu_assemble)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_TEXT, self.highlight_code, self.tab1.control)

        self.Show()
        self.tab1.control.DiscardEdits()
        self.on_new()

    def on_about(self, e):
        """
        Create an about message dialog box

        :param e:
        """
        dlg = wx.MessageDialog(self, " A SAP-1 code editor, assembler, and simulator \n in wxPython", "About SAP-1 IDE",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.

    def check_and_save(self, e):
        saved = wx.ID_OK
        if self.tab1.control.IsModified():
            exist_dlg = wx.MessageDialog(self, "Save current changes?", "Save changes " + self.filename,
                                         wx.YES_NO | wx.ICON_WARNING)
            if exist_dlg.ShowModal() == wx.ID_YES:
                saved = self.on_save(e)
            exist_dlg.Destroy()  # finally destroy it when finished.
        return saved

    def on_close(self, e):
        """
        Exit the application by closing the frame

        :param e:
        """
        if self.check_and_save(e) == wx.ID_OK:
            self.Destroy()

    def on_exit(self, e):
        """
        Exit the application by closing the frame

        :param e:
        """
        self.Close(True)  # Close the frame.

    def on_new(self, e=None):
        if self.check_and_save(e) == wx.ID_OK:
            self.tab2.reset_listing()
            self.tab3.reset_memory()
            self.tab1.control.Clear()
            self.tab1.control.DiscardEdits()
            self.filename = 'untitled'
            self.SetTitle(self.generate_title(self.filename))
            self.nb.SetSelection(0)

    def generate_title(self, filename):
        new_title = self.base_title
        if filename != '':
            new_title += " - "
            if self.tab1.control.IsModified():
                new_title += "*"
            new_title += filename
        return new_title

    def on_open(self, e):
        """ Open a file. Copy contents to the first tab text control and perform syntax highlighting
        :param e:
        """
        if self.check_and_save(e) == wx.ID_OK:
            dlg = wx.FileDialog(self, "Choose a file", self.directory_name, "", "*.*", wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.directory_name = dlg.GetDirectory()
                f = open(os.path.join(self.directory_name, self.filename), 'r')
                self.tab1.control.SetValue(f.read())
                f.close()
                self.highlight_code(e)
                self.tab1.control.SetModified(False)
                self.tab1.control.DiscardEdits()
                self.SetTitle(self.generate_title(self.filename))
                self.tab2.reset_listing()
                self.tab3.reset_memory()
                self.nb.SetSelection(0)
            dlg.Destroy()

    def write_file(self):
        """
        Save a file. Copy contents to the first tab text control and perform syntax highlighting
        :rtype: object
        """

        f = open(os.path.join(self.directory_name, self.filename), 'w')
        lines = self.tab1.control.GetValue()
        f.write(lines)
        f.close()
        self.tab1.control.SetModified(False)
        self.tab1.control.DiscardEdits()
        self.SetTitle(self.generate_title(self.filename))
        return wx.ID_OK

    def on_save(self, e):
        """ Save a file. Copy contents to the first tab text control and perform syntax highlighting
        :param e:
        """
        if self.filename == "untitled":
            saved = self.on_save_as(e)
        else:
            saved = self.write_file()
        return saved

    def on_save_as(self, e):
        """ Open a file. Copy contents to the first tab text control and perform syntax highlighting
        :param e:
        """
        saved = wx.ID_CANCEL
        dlg = wx.FileDialog(self, "Save file as...", self.directory_name, "", "*.*", wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.directory_name = dlg.GetDirectory()
            if os.path.exists(os.path.join(self.directory_name, self.filename)):
                exist_dlg = wx.MessageDialog(self, "Overwrite existing file?", "Save As " + self.filename,
                                             wx.YES_NO | wx.ICON_WARNING)
                if exist_dlg.ShowModal() == wx.ID_YES:
                    saved = self.write_file()
                exist_dlg.Destroy()  # finally destroy it when finished.
            else:
                saved = self.write_file()
        dlg.Destroy()
        return saved

    def on_assemble(self, e):
        """

        :param e:
        """
        a = Assembler()
        lines = self.tab1.control.GetValue()
        text = lines.split("\n")
        listing, memory_dump = a.assemble(text)
        errors = a.get_errors()
        self.tab2.control.Clear()
        for line in listing:
            self.tab2.control.AppendText(line)
        if len(errors):
            self.tab2.control.AppendText("\n")
            self.tab2.control.AppendText("ERRORS:\n")
            self.tab2.control.AppendText("\n")
            for line in errors:
                self.tab2.control.AppendText(line)
            self.nb.SetSelection(1)
        self.tab3.control.Clear()
        for line in memory_dump:
            self.tab3.control.AppendText(line)

    def is_valid_label(self, label):
        """
        Is this a valid label in the local symbol table

        :rtype: bool
        :param label: String Label to lookup in symbol table
        :return: true if label is found
        """
        found = False
        for x in self.symbol_table:
            if x == label:
                found = True
                break
        return found

    def highlight_code(self, e):
        """ need to make this be character based to better handle the attributes when typing.
            this would also fix the off by one errors I am seeing here and there
            :param e: """
        self.symbol_table = []
        font = self.tab1.control.GetFont()
        comment_attr = wx.TextAttr(self.color_database.Find("LIGHT GREY"), wx.WHITE, font=font)
        # label_attr = wx.TextAttr(self.color_database.Find("NAVY"), wx.WHITE, font=font)
        label_attr = wx.TextAttr(wx.BLUE, wx.WHITE, font=font)
        error_attr = wx.TextAttr(wx.WHITE, wx.RED, font=font)
        directive_attr = wx.TextAttr(self.color_database.Find("GOLD"), wx.WHITE, font=font)
        operand_attr = wx.TextAttr(wx.BLACK, wx.WHITE, font=font)

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
                        self.symbol_table.append(label)

        for i in range(0, max_line):
            line = self.tab1.control.GetLineText(i)
            length = self.tab1.control.GetLineLength(i)
            if line.startswith('#') or line.startswith(';'):
                self.tab1.control.SetStyle(start_of_line, (start_of_line + length), comment_attr)
            else:
                fields = line.split()

                if len(fields) > 0:
                    if fields[0].startswith('.'):
                        current_position = start_of_line + line.find(fields[0])
                        self.tab1.control.SetStyle(current_position, (current_position + (len(fields[0]))),
                                                   directive_attr)
                        if len(fields) > 1:
                            current_position = start_of_line + line.find(fields[1])
                            self.tab1.control.SetStyle(
                                current_position,
                                (current_position + len(fields[1])),
                                operand_attr)

                    elif fields[0].endswith(':'):
                        current_position = start_of_line + line.find(fields[0])
                        self.tab1.control.SetStyle(current_position, (current_position + len(fields[0])),
                                                   label_attr)
                        if len(fields) > 1:
                            if fields[1].startswith('.'):
                                current_position = start_of_line + line.find(fields[1])
                                self.tab1.control.SetStyle(current_position,
                                                           (current_position + len(fields[1])),
                                                           directive_attr)
                                if len(fields) > 2:
                                    current_position = start_of_line + line.find(fields[2])
                                    self.tab1.control.SetStyle(
                                        current_position,
                                        (current_position + len(fields[2])),
                                        operand_attr)

                            else:
                                current_position = start_of_line + line.find(fields[1])
                                self.tab1.control.SetStyle(current_position,
                                                           (current_position + len(fields[1])),
                                                           operator_attr)
                                if len(fields) == 3:
                                    target = make_target(fields[2])
                                    current_position = start_of_line + line.find(fields[2])
                                    if is_label(fields[2]):
                                        if self.is_valid_label(target):
                                            self.tab1.control.SetStyle(
                                                (current_position + 1),
                                                (current_position + len(target) + 1),
                                                label_attr)
                                        else:
                                            self.tab1.control.SetStyle(
                                                (current_position + 1),
                                                (current_position + len(target) + 1),
                                                error_attr)
                                    else:
                                        self.tab1.control.SetStyle(
                                            (current_position + 1),
                                            (current_position + len(target) + 1),
                                            operand_attr)

                    else:
                        current_position = start_of_line + line.find(fields[0])
                        self.tab1.control.SetStyle(current_position,
                                                   (current_position + len(fields[0])),
                                                   operator_attr)
                        if len(fields) == 2:
                            target = make_target(fields[1])
                            current_position = start_of_line + line.find(fields[1])
                            if is_label(fields[1]):
                                if self.is_valid_label(target):
                                    self.tab1.control.SetStyle((current_position + 1),
                                                               (current_position + len(target) + 1), label_attr)
                                else:
                                    self.tab1.control.SetStyle((current_position + 1),
                                                               (current_position + len(target) + 1), error_attr)
                            else:
                                self.tab1.control.SetStyle(
                                    (current_position + 1),
                                    (current_position + len(target)),
                                    operand_attr)

            start_of_line += length + 1

        self.SetTitle(self.generate_title(self.filename))


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, "SAP-1 IDE")
    app.MainLoop()
