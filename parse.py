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
        self.name_arg = {}

    def name(self):
        """name = letter, { letter | digit } ;"""
        if self.symbol.type == self.scanner.NAME:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()     # invalid device name

    def device(self):
        """device = "DTYPE" | "XOR" ;"""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.SEMICOLON:
            self.syntax_error()     # unexpected symbol

    def device_arg(self):
        """device_arg = "CLOCK" | "AND" | "NAND" | "OR" | "NOR" | "SWITCH" ;"""
        current_id = self.symbol.id     # save it to local variable current_id
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.OPENBRACKET:    # NOR(
            self.symbol = self.scanner.get_symbol()
        else:                                               # NOR or NOR@
            self.syntax_error()     # missing argument of device_arg
        if self.symbol.type == self.scanner.NUMBER:
            if (current_id == self.scanner.AND_ID or self.scanner.NAND_ID
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
                    self.semantic_error()   # invalid argument
        else:                                               # NOR(A)
            self.syntax_error()     # invalid argument type
        if self.symbol.type == self.scanner.CLOSEDBRACKET:  # NOR(2)
            self.symbol = self.scanner.get_symbol()
            return arg_val     # output number of arguments
        else:
            self.syntax_error()     # missing symbols: )

    def assignment(self):
        """assignment = name, { "," , name }, "=",
        ( device_arg_dec | device ), ";" ;"""
        name_id = self.symbol.id     # local variable to save name id
        if name_id == 0:     # name_id is already taken: needs working
            self.semantic_error()    # used name in device declaration
        else:
            self.name()
        while self.symbol.type == self.scanner.COMMA:
            self.symbol = self.scanner.get_symbol()
            self.name()
        if self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DEVICE_ARG:
                x = self.device_arg()
            elif self.symbol.type == self.scanner.DEVICE:
                self.device()
            else:
                self.sytax_error()    # unrecognised device type
        else:
            self.syntax_error()     # missing symbols: =
        if self.symbol.type == self.scanner.SEMICOLON:
            # save argument to name_id in dictionary
            self.name_arg[name_id] = x
        else:
            self.syntax_error()     # missing symbols: ;

    def connection(self):
        if self.symbol.type == self.scanner.NAME:
            self.name()
        elif self.symbol.type == self.scanner.
        if self.symbol.type == self.scanner.ARROW:
            self.symbol = self.scanner.get_symbol()



    def section_dev(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id == self.scanner.DEVICES_ID):
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.OPENCURLYBRACKET:
                self.symbol = self.scanner.get_symbol()
                self.assigment()
                while self.symbol.type == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type != self.scanner.CLOSEDCURLYBRACKET:
                        self.assignment()
                    else:
                        break
                if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
                    self.symbol = self.scanner.get_symbol()
                else:
                    self.syntax_error()     # missing symbols: }

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        return True
