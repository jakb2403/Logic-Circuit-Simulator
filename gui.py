"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
from wx.core import ROLE_SYSTEM_TOOLBAR
import wx.glcanvas as wxcanvas
import wx.lib.agw.aui as aui
from OpenGL import GL, GLUT, GLU

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    """

    def __init__(self, parent, devices, monitors):
        """Initialise canvas properties and useful variables."""

        self.devices = devices
        self.monitors = monitors

        super().__init__(parent, -1,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        counter = 1
        # for device_id, output_id in self.monitors.monitors_dictionary:
        #     monitor_name = self.devices.get_signal_name(device_id, output_id)
        #     signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
        #     self.render_text(monitor_name, 10, (10+150*counter))
        #     for signal in signal_list:
        #         x = (i * 20) + 10
        #         x_next = (i * 20) + 30
        #         if signal == self.devices.HIGH:
        #             y = 100
        #         if signal == self.devices.LOW:
        #             y = 75
        #         if signal == self.devices.RISING:

        #         if signal == self.devices.FALLING:

        #         if signal == self.devices.BLANK:

        #     counter += 1

        # for signal in signals_to_draw:
        #     # Draw specified text at position (10, 10)
        #     self.render_text(signal_name_text, 10, 10)
        #     # Draw a sample signal trace
        #     GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
        #     GL.glBegin(GL.GL_LINE_STRIP)
        #     for i in range(len(signal)):
        #         x = (i * 20) + 10
        #         x_next = (i * 20) + 30
        #         if signal[i] == 0:
        #             y = 75
        #         else:
        #             y = 100
        #         GL.glVertex2f(x, y)
        #         GL.glVertex2f(x_next, y)
        #     GL.glEnd()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(["Mouse button pressed at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join(["Mouse button released at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join(["Mouse left canvas at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(["Mouse dragged to: ", str(event.GetX()),
                            ", ", str(event.GetY()), ". Pan is now: ",
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Negative mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Positive mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))


class TopMenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.YELLOW)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create widgets
        cycles_text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        run_button = wx.Button(self, wx.ID_ANY, "Run")
        pause_button = wx.Button(self, wx.ID_ANY, "Pause")
        continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        load_button = wx.Button(self, wx.ID_ANY, "Load")
        exit_button = wx.Button(self, wx.ID_ANY, "Exit")

        # Add widgets to sizer
        self.sizer.Add(run_button, 1, wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(cycles_text, 0, wx.LEFT | wx.RIGHT |
                       wx.ALIGN_CENTER_VERTICAL, 1)
        self.sizer.Add(spin, 1, wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(pause_button, 1, wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(continue_button, 1, wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(load_button, 1, wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(exit_button, 1, wx.LEFT | wx.RIGHT, 5)

        # Bind events to event handlers
        spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        run_button.Bind(wx.EVT_BUTTON, self.on_run_button)        
        load_button.Bind(wx.EVT_BUTTON, self.on_click_load)
        exit_button.Bind(wx.EVT_BUTTON, self.on_click_exit)

        self.SetSizer(self.sizer)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        

    # def on_click_add(self, event):
    #     """Handle the event when the user clicks the 'Add' button after selecting a signal"""
    #     device_to_add = self.mon_add_dropdown.GetValue()
    #     device_index = self.available_devices.index(device_to_add)
    #     del self.available_devices[device_index]
    #     self.mon_add_dropdown.Delete(device_index)
    #     self.mon_add_dropdown.SetSelection(0)
    #     text = "".join(["Signal added: ", device_to_add])
    #     

    def on_click_load(self, event):
        """Handle the event when the user clicks the 'Load' button"""
        with wx.FileDialog(self, "Load .txt file", wildcard=".txt files (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            text = "".join(["Opening file: ", pathname])
            

    def on_click_exit(self, event):
        """Handle the event when the user clicks the 'Exit' button"""
        self.Close()


class SidebarPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.RED)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.devices_list = ["G1", "G2", "G3", "G4"]
        self.device_types_list = ["All", "AND", "NAND",
                                  "OR", "NOR", "XOR", "SWITCH", "CLOCK", "DTYPE"]
        self.available_devices = self.devices_list

        # Create widgets
        device_type = wx.StaticText(self, wx.ID_ANY, "Device type")
        mon_add_dropdown = wx.ComboBox(
            self, choices=self.device_types_list, style=wx.CB_READONLY)
        monitor_checklist = wx.CheckListBox(
            self, choices=self.available_devices, name="Monitor Signals")

        # Add widgets to sizer
        # sidebar_sizer.Add(sidebar_notebook, 0, wx.ALL, 0)
        # sidebar_panel.SetSizer(sidebar_sizer)
        self.sizer.Add(device_type, 0, wx.ALL, 0)
        self.sizer.Add(mon_add_dropdown, 0,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 0)
        self.sizer.Add(monitor_checklist, 1,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 0)

        # Bind events to event handlers
        mon_add_dropdown.Bind(wx.EVT_COMBOBOX, self.on_dropdown)        

        self.SetSizer(self.sizer)

    def on_dropdown(self, event):
        """Handle the event when the user clicks the dropdown menu to add a
        monitor signal"""
        self.device_to_add = self.mon_add_dropdown.GetValue()
        text = "".join(["Signal type to display: ", self.signal_to_add])


class CmdPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.GREEN)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create sizers for input and output
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create widgets
        self.cmd_output_text_box = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.com_text = wx.StaticText(self, wx.ID_ANY, "$")
        self.cmd_input_text_box = wx.TextCtrl(self, wx.BOTTOM, "",
                                              style=wx.TE_PROCESS_ENTER)

        # Add widgets to sizer
        output_sizer.Add(self.cmd_output_text_box, 0, wx.EXPAND, 0)
        # TODO to set value of textbox: self.textpanel.SetValue(s)
        input_sizer.Add(self.com_text, 0, wx.LEFT |
                        wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 12)
        input_sizer.Add(self.cmd_input_text_box, 1, wx.RIGHT, 5)

        # Add sub-sizers to main sizer
        self.sizer.Add(output_sizer, 1, wx.EXPAND, 0)
        self.sizer.Add(input_sizer, 0, wx.EXPAND, 0)

        # Bind events to event handlers
        self.cmd_input_text_box.Bind(wx.EVT_TEXT_ENTER, self.on_cmd_enter)

        self.SetSizer(self.sizer)

    def on_cmd_enter(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.cmd_input_text_box.GetValue()
        self.cmd_input_text_box.Clear()
        self.cmd_output_text_box.AppendText("\n $  " + text_box_value)
        text = "".join(["New text box value: ", text_box_value])
        


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))
        
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        
        self.SetFont(wx.Font(13, wx.FONTFAMILY_TELETYPE,
                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                     'Courier'))
        # Create AUI manager
        self.mgr = aui.AuiManager()
        # Set the window that the AUI manages
        self.mgr.SetManagedWindow(self)
        
        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Configure the toolbar
        self.toolbar = self.CreateToolBar()
        self.run_button = self.toolbar.AddTool(wx.ID_ANY, "Run", wx.Bitmap("icons/run.png")) 
        self.open_button = self.toolbar.AddTool(wx.ID_ANY, "Load", wx.Bitmap("icons/folder.png")) 

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        self.sidebar = SidebarPanel(self)
        self.cmd = CmdPanel(self)

        self.mgr.AddPane(self.canvas, aui.AuiPaneInfo().CenterPane())
        self.mgr.AddPane(self.sidebar, aui.AuiPaneInfo().Left().Floatable(False))
        self.mgr.AddPane(self.cmd, aui.AuiPaneInfo().Bottom().Floatable(False))

        # Set docking guides (THIS FIXES THE FLOATING POINT PROBLEM)
        agwFlags = self.mgr.GetAGWFlags()
        self.mgr.SetAGWFlags(agwFlags | aui.AUI_MGR_AERO_DOCKING_GUIDES)

        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.toolbar.Realize()
        self.Centre()
        self.Show(True)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)

    def on_close(self, event):
        # deinitialise the frame manager
        self.mgr.UnInit()
        self.Destroy()