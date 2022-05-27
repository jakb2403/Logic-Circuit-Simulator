"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import scanner
import devices
import network


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

    def name(self):
        """name = letter, { letter | digit } ;"""
        if self.symbol.type == self.scanner.NAME:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()     # invalid device name

    def argument(self):
        """argument = digit , { digit } ;"""
        while self.symbol.type == self.scanner.NUMBER:
            self.symbol = self.scanner.get_symbol()

    def input(self):
        """input = name, ".", "I", argument ;"""
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
        self.name()
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error() # missing symbols: .
        if self.symbol.type == self.scanner.DTYPE_IP:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()  # unrecognised dtype_ip
    
    def dtype_op(self):
        self.name()
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error() # missing symbols: .
        if self.symbol.type == self.scanner.DTYPE_OP:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()  # unrecognised dtype_op

    def device(self):
        """device = "DTYPE" | "XOR" ;"""
        """device_arg = "CLOCK" | "AND" | "NAND" | "OR" | "NOR" | "SWITCH" ;"""
        if self.symbol.type == self.scanner.DEVICE:
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.DEVICE_ARG:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.OPENBRACKET:
                self.symbol = self.scanner.get_symbol()
            else:
                self.syntax_error()     # missing argument of device_arg
            if self.symbol.type == self.scanner.NUMBER:
                self.argument()
            else:
                self.syntax_eror()      # invalid argument type
            if self.symbol.type == self.scanner.CLOSEDBRACKET:
                self.symbol = self.scanner.get_symbol()
            else:
                self.syntax_error()     # missing symbols: )
        else:
            self.syntax_error()  # unrecognised device type

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
                    self.semantic_error()   # invalid argument            """

    def assignment(self):
        """assignment = name, { "," , name }, "=",
        ( device_arg_dec | device ), ";" ;"""
        st_type = "assigment"
        self.name()
        while self.symbol.type == self.scanner.COMMA:
            self.symbol = self.scanner.get_symbol()
            self.name()
        if self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            self.device()
        else:
            self.syntax_error()     # missing symbols: =
        if self.symbol.type == self.scanner.SEMICOLON:
            return st_type
        else:
            self.syntax_error()     # missing symbols: ;

    def connection(self):
        i = 0
        self.name()
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
            elif (self.symbol.type == self.scanner.KEYWORD
                  and self.symbol.id == self.scanner.I_ID):
                i = 1
            elif self.symbol.type == self.scanner.DTYPE_IP:
                i = 2
            else:
                self.syntax_error()  # unexpected symbols: .
        if self.symbol.type == self.scanner.ARROW:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()  # missing symbols: ->
        if self.symbol.type == self.scanner.NAME:
            self.input()
        


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
