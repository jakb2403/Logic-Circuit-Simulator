"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        self.error_count = 0
        [self.output_to_output, self.input_to_input, self.input_to_output,
         self.invalid_device_name, self.invalid_device_inOut_name,
         self.unrecognised_device_type, self.invalid_argument_type,
         self.missing_argument, self.missing_keyword,
         self.missing_symbol,
         self.section_order_error] = self.names.unique_error_codes(12)

        self.keyword = [self.scanner.DEVICES_ID,
                        self.scanner.CONNECT_ID,
                        self.scanner.MONITOR_ID]

    def syntax_error(self, error_type, dev=None, sym=None):
        """Print error type and count total number of syntax 
        errors."""
        self.error_count += 1
        print("Syntax_error: ", end="")
        if error_type == self.output_to_output:
            print("output connected to output")
        elif error_type == self.input_to_input:
            print("input connected to input")
        elif error_type == self.input_to_output:
            print("input connected to output")
        elif error_type == self.invalid_device_name:
            print("invalid device name")
        elif error_type == self.invalid_device_inOut_name:
            print("invalid input/output name")
        elif error_type == self.unrecognised_device_type:
            print("unrecognised device type")
        elif error_type == self.invalid_argument_type:
            print("expected argument to be an integer")
        elif error_type == self.missing_argument:
            print("missing argument for device type: " + dev)
        elif error_type == self.missing_symbol:
            print("missing symbol: " + sym)
        elif error_type == self.missing_keyword:
            print("missing keyword")
        elif error_type == self.section_order_error:
            print("incorrect ordering of sections")
        while (self.symbol.type != self.scanner.SEMICOLON
                and self.symbol.type != self.scanner.EOF):
            self.symbol = self.scanner.get_symbol()

    def name(self):
        """Pass when symbol is name."""
        if self.symbol.type == self.scanner.NAME:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.invalid_device_name)

    def argument(self):
        """Pass until symbol is not number."""
        if self.symbol.type == self.scanner.NUMBER:
            self.symbol = self.scanner.get_symbol()
            return int(self.symbol.id)
        else:
            self.syntax_error(self.invalid_argument_type)

    def inputOrOutput(self, st_type):
        # st_type has to be one of "conlhs", "conrhs", and "mon"
        """Return True if output and false if input"""
        self.name()
        if st_type == "conlhs":
            if self.symbol.type == self.scanner.ARROW:
                return True     # True means output
        elif st_type == "conrhs":
            if (self.symbol.type == self.scanner.COMMA
                    or self.symbol.type == self.scanner.SEMICOLON):
                return True
        elif st_type == "mon":
            if self.symbol.type == self.scanner.SEMICOLON:
                return True
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
                return True
            elif self.symbol.type == self.scanner.DTYPE_IP:
                self.symbol = self.scanner.get_symbol()
                return False     # False means input
            elif (self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.I_id):
                self.argument()
                return False
            else:
                self.syntax_error(self.invalid_device_inOut_name)
        else:
            self.syntax_error(self.missing_symbol, sym=".")

    def device(self):
        """device = "DTYPE" | "XOR" ;"""
        """device_arg = "CLOCK" | "AND" | "NAND" | "OR" | "NOR" | "SWITCH" ;"""
        if self.symbol.type == self.scanner.DEVICE:
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.DEVICE_ARG:
            x = self.scanner.id
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.OPENBRACKET:
                self.symbol = self.scanner.get_symbol()
            else:
                self.syntax_error(self.missing_argument, dev=x)
            self.argument()
            if self.symbol.type == self.scanner.CLOSEDBRACKET:
                self.symbol = self.scanner.get_symbol()
            else:
                self.syntax_error(self.missing_symbol, sym=")")
        else:
            self.syntax_error(self.unrecognised_device_type)

    def assignment(self):
        """assignment = name, { "," , name }, "=",
        ( device_arg_dec | device ), ";" ;"""
        self.name()
        while self.symbol.type == self.scanner.COMMA:
            self.symbol = self.scanner.get_symbol()
            self.name()
            if self.symbol.type == self.scanner.EOF:
                break
        if self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            self.device()
        else:
            self.syntax_error(self.missing_symbol, sym="=")
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            self.syntax_error(self.missing_symbol, sym=";")

    def connection(self):
        """connection = ( name | dtype_op), "->", ( input | dtype_ip ),
        { "," , ( input | dtype_ip ) }, ";" ;"""
        x = self.inputOrOutput("conlhs")
        if self.symbol.type == self.scanner.ARROW:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="->")
        y = self.inputOrOutput("conrhs")
        if x is True and y is False:
            while self.symbol.type == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                z = self.inputOrOutput("conrhs")
                if z is True:
                    self.syntax_error(self.output_to_output)
                if self.symbol == self.scanner.EOF:
                    break
        elif x is True and y is True:
            self.syntax_error(self.output_to_output)
        elif x is False and y is False:
            self.syntax_error(self.input_to_input)
        else:
            self.syntax_error(self.input_to_output)
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            self.syntax_error(self.missing_symbol, sym=";")

    def monitor(self):
        """monitor = monitor_name, "=", ( name | input ), ";" ;"""
        self.inputOrOutput("mon")
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            self.syntax_error(self.missing_symbol, ";")

    def section(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id in self.keyword):
            sec_def = self.symbol.id
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_keyword)
        if self.symbol.type == self.scanner.OPENCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="{")
        if sec_def == self.scanner.DEVICES_ID:
            self.assignment()
        elif sec_def == self.scanner.CONNECT_ID:
            self.connection()
        else:
            self.monitor()
        indic = True
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
                indic = False
                break
            elif (self.symbol.type == self.scanner.KEYWORD and
                    self.symbol.id in self.keyword and indic is True):
                break
            elif self.symbol.type == self.scanner.EOF:
                break
            else:
                if sec_def == self.scanner.DEVICES_ID:
                    self.assignment()
                elif sec_def == self.scanner.CONNECT_ID:
                    self.connection()
                else:
                    self.monitor()
        if indic is False:
            self.symbol = self.scanner.get_symbol()
            return sec_def
        else:
            self.syntax_error(self.missing_symbol, sym="}")

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        self.symbol = self.scanner.get_symbol()
        dev = self.section()
        con = self.section()
        mon = self.section()
        if dev != self.scanner.DEVICES_ID:
            self.syntax_error(self.section_order_error)
        if con != self.scanner.CONNECT_ID:
            self.syntax_error(self.section_order_error)
        if mon != self.scanner.MONITOR_ID:
            self.syntax_error(self.section_order_error)
        if self.error_count == 0:
            return True
        else:
            return False
