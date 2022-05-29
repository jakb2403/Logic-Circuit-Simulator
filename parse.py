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
         self.invalid_device_name, self.invalid_monitor_name,
         self.invalid_device_input_name, self.unrecognised_device_type,
         self.invalid_argument_type, self.missing_argument,
         self.missing_symbol, self.unexpected_symbol,
         self.section_order_error] = self.names.unique_error_codes()

    def syntax_error(self, error_type, dev=None, sym=None):
        """print error type and count total number of syntax errors"""
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
        elif error_type == self.invalid_monitor_name:
            print("invalid monitor name")
        elif error_type == self.invalid_device_input_name:
            print("invalid input name")
        elif error_type == self.unrecognised_device_type:
            print("unrecognised device type")
        elif error_type == self.invalid_argument_type:
            print("expected argument to be an integer")
        elif error_type == self.missing_argument:
            print("missing argument for device type: " + dev)
        elif error_type == self.missing_symbol:
            print("missing symbol: " + sym)
        elif error_type == self.unexpected_symbol:
            print("unexpected symbol")   # ideally, we don't need this one
        elif error_type == self.section_order_error:
            print("incorrect ordering of sections")
        while (self.symbol.type != self.scanner.SEMICOLON
                and self.symbol.type != self.scanner.EOF):
            self.symbol = self.scanner.get_symbol()

    def name(self):
        """name = letter, { letter | digit } ;"""
        if self.symbol.type == self.scanner.NAME:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.invalid_device_name)

    def argument(self):
        """argument = digit , { digit } ;"""
        if self.symbol.type == self.scanner.NUMBER:
            self.symbol = self.scanner.get_symbol()
            while self.symbol.type == self.scanner.NUMBER:
                self.symbol = self.scanner.get_symbol()
                if self.symbol == self.scanner.EOF:
                    break
        else:
            self.syntax_error(self.invalid_argument_type)

    """    def input(self):
                input = name, ".", "I", argument ;
                self.name()
                if self.symbol.type == self.scanner.DOT:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()  # missing symbols: .
                if (self.symbol.type == self.scanner.KEYWORD
                        and self.symbol.id == self.scanner.I_id):
                    self.argument()
                else:
                    self.syntax_error()  # invalid device input name

            def dtype_ip(self):
                dtype_ip = name, ".", dtype_ip_name ;
                self.name()
                if self.symbol.type == self.scanner.DOT:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()   # missing symbols: .
                if self.symbol.type == self.scanner.DTYPE_IP:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()  # unrecognised dtype input

            def dtype_op(self):
                dtype_op = name, ".", dtype_op_name ;
                self.name()
                if self.symbol.type == self.scanner.DOT:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()   # missing symbols: .
                if self.symbol.type == self.scanner.DTYPE_OP:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()  # unrecognised dtype output    """

    def monitor_name(self):
        """monitor_name = "MON", argument ;"""
        if (self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.MON_id):
            self.symbol = self.scanner.get_symbol()
            self.argument()
        else:
            self.syntax_error(self.invalid_monitor_name)

    def nameOrDtypeOP(self):
        self.name()
        if self.symbol.type == self.scanner.ARROW:
            return True
        elif self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
                return True
            elif self.symbol.type == self.scanner.DTYPE_IP:
                self.symbol = self.scanner.get_symbol()
                return False
            elif (self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.I_id):
                self.argument()
                return False
            else:
                self.syntax_error(self.unexpected_symbol)  # .
        else:
            self.syntax_error(self.unexpected_symbol)

    def inputOrDtypeIP(self):
        self.name()
        if (self.symbol.type == self.scanner.COMMA
                or self.symbol.type == self.scanner.SEMICOLON):
            return False
        elif self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
                return False
            elif self.symbol.type == self.scanner.DTYPE_IP:
                self.symbol = self.scanner.get_symbol()
                return True
            elif (self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.I_id):
                self.argument()
                return True
            else:
                self.syntax_error(self.unexpected_symbol)
        else:
            self.syntax_error(self.unexpected_symbol)

    def monitor_point(self):
        self.name()
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        elif self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
            elif self.symbol.type == self.scanner.DTYPE_IP:
                self.symbol = self.scanner.get_symbol()
            elif (self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.I_id):
                self.argument()
            else:
                self.syntax_error(self.unexpected_symbol)
        else:
            self.syntax_error(self.unexpected_symbol)

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
                self.syntax_error(self.missing_argument, sym=")")
        else:
            self.syntax_error(self.unrecognised_device_type)

    """     if (current_id == self.scanner.AND_ID or self.scanner.NAND_ID
                    or self.scanner.OR_ID or self.scanner.NOR_ID):
                if 2 <= self.symbol.id <= 16:               # NOR(2
                    arg_val = self.symbol.id
                    self.symbol = self.scanner.get_symbol()
                else:                                       # NOR(18
                    self.semantic_error()   # invalid argument
            elif current_id == self.scanner.SWITCH_ID:      # SWITCH(1
                if self.symbol == 0 or 1:
                    arg_val = self.symbol.id
                    self.symbol = self.scanner.get_symbol()
                else:                                       # SWITCH(3
                    self.semantic_error()   # invalid argument
            elif current_id == self.scanner.CLOCK_ID:       # CLOCK(20
                if self.symbol < 10000:     # limit clock cycle to 10000
                    arg_val = self.symbol.id
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.semantic_error()   # invalid argument    """

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
        x = self.nameOrDtypeOP()
        if self.symbol.type == self.scanner.ARROW:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="->")
        y = self.inputOrDtypeIP()
        if x is True and y is True:
            while self.symbol.type == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                z = self.inputOrDtypeIP()
                if z is False:
                    self.syntax_error(self.output_to_output)
                if self.symbol == self.scanner.EOF:
                    break
        elif x is True and y is False:
            self.syntax_error(self.output_to_output)
        elif x is False and y is True:
            self.syntax_error(self.input_to_input)
        else:
            self.syntax_error(self.input_to_output)
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            self.syntax_error(self.missing_symbol, sym=";")

    def monitor(self):
        """monitor = monitor_name, "=", ( name | input ), ";" ;"""
        self.monitor_name()
        if self.symbol.type == self.scanner.EQUALS:
            self.monitor_point()
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            self.syntax_error(self.missing_symbol, ";")

    def section_dev(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id == self.scanner.DEVICES_ID):
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.section_order_error)
        if self.symbol.type == self.scanner.OPENCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="{")
        self.assignment()
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CLOSEDCURLYBRACKET
                    or self.symbol.type == self.scanner.EOF):
                break
            else:
                self.assignment()
        if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="}")

    def section_con(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id == self.scanner.CONNECT_ID):
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.section_order_error)
        if self.symbol.type == self.scanner.OPENCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="{")
        self.connection()
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CLOSEDCURLYBRACKET
                    or self.symbol.type == self.scanner.EOF):
                break
            else:
                self.connection()
        if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="}")

    def section_mon(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id == self.scanner.MONITOR_ID):
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.section_order_error)
        if self.symbol.type == self.scanner.OPENCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="{")
        self.monitor()
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CLOSEDCURLYBRACKET
                    or self.symbol.type == self.scanner.EOF):
                break
            else:
                self.monitor()
        if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="}")

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        self.symbol = self.scanner.get_symbol()
        self.section_dev()
        self.section_con()
        self.section_mon()
        if self.error_count == 0:
            return True
        else:
            return False
