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

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        
        return True

    def assignment(self):
        """assignment = name, { "," , name }, "=", ( device_arg_dec | device ), ";" ;"""
        self.name()
        while self.symbol.type == self.scanner.COMMA: # missing comma should also raise error: missing symbols, or maybe not
            self.symbol = self.scanner.get_symbol()
            self.name()
        if self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DEVICE_ARG:
                self.device_arg()
            elif self.symbol.type == self.scanner.DEVICE:
                self.device()
            else:
                self.sytax_error() # unrecognised device type
        else: 
            self.syntax_error() # missing symbols: =
        if self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error() # missing symbols: ;
        
    def name(self):
        """name = letter, { letter | digit } ;"""
        if self.symbol.type == self.scanner.NAME:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error() # invalid device name
    
    def device_arg(self):
        """device_arg = "CLOCK" | "AND" | "NAND" | "OR" | "NOR" | "SWITCH" ;"""
        current_id = self.symbol.id # save device_arg_id to local variable current_id
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.OPENBRACKET:    # NOR(
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.NUMBER:       # NOR2
            self.syntax_error() # missing symbols: (
        else:                                               # NOR or NOR@
            self.syntax_error() # missing argument of device_arg
        if self.symbol.type == self.scanner.NUMBER:         
            if (current_id == self.scanner.ADD_ID or self.scanner.NAND_ID 
                or self.scanner.OR_ID or self.scanner.NOR_ID):
                if 2 <= self.symbol.id <= 16:               # NOR(2
                    ret
                    self.symbol = self.scanner.get_symbol()
                else:                                       # NOR(18
                    self.semantic_error() # invalid argument
            elif current_id == self.scanner.SWITCH_ID:      # SWITCH(1
                if self.symbol == 0 or 1:
                    self.symbol = self.scanner.get_symbol() 
                else:                                       # SWITCH(3
                    self.semantic_error() # invalid argument
            elif current_id == self.scanner.CLOCK_ID:       # CLOCK(20
                self.symbol = self.scanner.get_symbol()     # not sure whether negative number passes so might need error handling
        else:                                               # NOR(A)
            self.syntax_error() # invalid argument type
        if self.symbol.type == self.scanner.CLOSEDBRACKET:  # NOR(2)
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error() # missing symbols: )
    
    def device(self):
        """device = "DTYPE" | "XOR" ;"""
        self.symbol = self.scanner.get_symbol()
        if self.symbol == self.scanner.OPENBRACKET:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.NUMBER:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.CLOSEDBRACKET:
                    self.syntax_error() # argument to device
"""                else:
                    self.syntax_error() #unexpected symbol: (
            else:
                self.syntax_error() # unexpected symbol: ("""
        