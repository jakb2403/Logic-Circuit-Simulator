"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import wx.glcanvas as wxcanvas
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
        self.SetFont(wx.Font(13, wx.FONTFAMILY_TELETYPE,
                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                     'Courier'))

        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors

        # self.devices_list = devices.devices_list
        self.device_types_list = ["All", "AND", "NAND",
                                  "OR", "NOR", "XOR", "SWITCH", "CLOCK", "DTYPE"]
        self.devices_list = ["View all", "G1", "G2", "G3", "G4"]
        self.available_devices = self.devices_list

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Configure the widgets
        # Top menu
        self.cycles_text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.device_type = wx.StaticText(self, wx.ID_ANY, "Device type")
        self.com_text = wx.StaticText(self, wx.ID_ANY, "$")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.pause_button = wx.Button(self, wx.ID_ANY, "Pause")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.load_button = wx.Button(self, wx.ID_ANY, "Load")
        self.exit_button = wx.Button(self, wx.ID_ANY, "Exit")
        # Sidebar
        self.mon_add_dropdown = wx.ComboBox(
            self, choices=self.device_types_list, style=wx.CB_READONLY)
        self.monitor_checklist = wx.CheckListBox(
            self, choices=self.available_devices, name="Monitor Signals")
        # Terminal output
        self.cmd_output_text_box = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # Terminal input
        self.cmd_input_text_box = wx.TextCtrl(self, wx.BOTTOM, "",
                                              style=wx.TE_PROCESS_ENTER)

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.cmd_input_text_box.Bind(wx.EVT_TEXT_ENTER, self.on_cmd_enter)
        self.load_button.Bind(wx.EVT_BUTTON, self.on_click_load)
        self.exit_button.Bind(wx.EVT_BUTTON, self.on_click_exit)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_menu_sizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sidebar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sidebar_sizer = wx.BoxSizer(wx.VERTICAL)
        cmd_output_sizer = wx.BoxSizer(wx.VERTICAL)
        cmd_input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(top_menu_sizer, 0, wx.TOP | wx.EXPAND, 5)
        main_sizer.Add(canvas_sidebar_sizer, 1, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(cmd_output_sizer, 0, wx.EXPAND, 5)
        main_sizer.Add(cmd_input_sizer, 0, wx.BOTTOM | wx.EXPAND, 5)

        top_menu_sizer.Add(self.run_button, 1, wx.LEFT | wx.RIGHT, 5)
        top_menu_sizer.Add(self.cycles_text, 0, wx.LEFT | wx.RIGHT |
                           wx.ALIGN_CENTER_VERTICAL, 1)
        top_menu_sizer.Add(self.spin, 1, wx.LEFT | wx.RIGHT, 5)
        top_menu_sizer.Add(self.pause_button, 1, wx.LEFT | wx.RIGHT, 5)
        top_menu_sizer.Add(self.continue_button, 1, wx.LEFT | wx.RIGHT, 5)
        top_menu_sizer.Add(self.load_button, 1, wx.LEFT | wx.RIGHT, 5)
        top_menu_sizer.Add(self.exit_button, 1, wx.LEFT | wx.RIGHT, 5)

        canvas_sidebar_sizer.Add(
            self.canvas, 4, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        canvas_sidebar_sizer.Add(sidebar_sizer, 1, wx.LEFT | wx.RIGHT, 5)

        sidebar_sizer.Add(self.device_type, 0, wx.ALL, 0)
        sidebar_sizer.Add(self.mon_add_dropdown, 0,
                          wx.EXPAND | wx.LEFT | wx.RIGHT, 0)
        sidebar_sizer.Add(self.monitor_checklist, 1,
                          wx.EXPAND | wx.LEFT | wx.RIGHT, 0)

        cmd_output_sizer.Add(self.cmd_output_text_box, 0, wx.EXPAND, 0)
        # TODO to set value of textbox: self.textpanel.SetValue(s)

        cmd_input_sizer.Add(self.com_text, 0, wx.LEFT |
                            wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 12)
        cmd_input_sizer.Add(self.cmd_input_text_box, 1, wx.RIGHT, 5)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_cmd_enter(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.cmd_input_text_box.GetValue()
        self.cmd_input_text_box.Clear()
        self.cmd_output_text_box.AppendText("\n $  " + text_box_value)
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def on_dropdown(self, event):
        """Handle the event when the user clicks the dropdown menu to add a
        monitor signal"""
        self.device_to_add = self.mon_add_dropdown.GetValue()
        text = "".join(["Signal to add: ", self.signal_to_add])
        self.canvas.render(text)

    def on_click_add(self, event):
        """Handle the event when the user clicks the 'Add' button after selecting a signal"""
        device_to_add = self.mon_add_dropdown.GetValue()
        device_index = self.available_devices.index(device_to_add)
        del self.available_devices[device_index]
        self.mon_add_dropdown.Delete(device_index)
        self.mon_add_dropdown.SetSelection(0)
        text = "".join(["Signal added: ", device_to_add])
        self.canvas.render(text)

    def on_click_load(self, event):
        """Handle the event when the user clicks the 'Load' button"""
        with wx.FileDialog(self, "Load .txt file", wildcard=".txt files (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            text = "".join(["Opening file: ", pathname])
            self.canvas.render(text)

    def on_click_exit(self, event):
        """Handle the event when the user clicks the 'Exit' button"""
        self.Close()
