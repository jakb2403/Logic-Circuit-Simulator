"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import sys
import os

from prelim.exercise import get_next_character

class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None
        self.line = None
        self.pos = None
        self.init_state = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.path = os.path.basename(path)
        self.names = names
        self.symbol_type_list = [
            self.DOT,
            self.COMMA,
            self.SEMICOLON,
            self.EQUALS,
            self.ARROW,
            self.BAR,
            self.OPENBRACKET,
            self.CLOSEDBRACKET,
            self.OPENCURLYBRACKET,
            self.CLOSEDCURLYBRACKET,
            self.KEYWORD,
            self.DEVICE_ARG,
            self.DEVICE,
            self.DTYPE_IP,
            self.DTYPE_OP,
            self.NUMBER,
            self.NAME,
            self.EOF] = range(18)  
        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", 
                                "MON", "I", "END"]
        self.device_arg_list = ["CLOCK", "AND", "NAND", "OR", "NOR", "SWITCH"]
        self.device_list = ["DTYPE", "XOR"]
        self.dtype_ip_list = ["SET", "CLEAR", "DATA", "CLK"]
        self.dtype_op_list = ["Q", "QBAR"]

        try:
            self.file = open(self.path, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()

    def get_next_character(self):
        """Read and return the next character in input_file."""
        return(self.file.read(1))

    def skip_spaces(self):
        """Seek and return the next non-whitespace character in input_file."""
        nwc = get_next_character()
        if nwc.isspace() is True:
            return("")
        else:
            return(nwc)

    def error_found(self):
        """Outputs the current line and a ^ symbol on the next line to
        highlight the location of the error"""
        pass

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.current_character = self.skip_spaces()

        #if symbol is a name
        if self.current_character.isalpha():
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
                #symbol.line = 
                #symbol.pos = 
            else:
                symbol.type = self.NAME
                [symbol.id] = self.names.lookup([name_string])
                #symbol.line = 
                #symbol.pos = 

        #if symbol is a number
        elif self.current_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER
            #symbol.line = 
            #symbol.pos = 

        #if symbol is a dot
        elif self.current_character == ".":
            symbol.type = self.DOT
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is a comma
        elif self.current_character == ",":
            symbol.type = self.COMMA
            #symbol.line = 
            #symbol.pos = 
            self.advance()    

        #if symbol is a semicolon
        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is a equals
        elif self.current_character == "=":
            symbol.type = self.EQUALS
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an arrow
        elif self.current_character == "->":
            symbol.type = self.ARROW
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is a bar
        elif self.current_character == "|":
            symbol.type = self.BAR
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an openbracket
        elif self.current_character == "(":
            symbol.type = self.OPENBRACKET
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an closedbracket
        elif self.current_character == ")":
            symbol.type = self.CLOSEDBRACKET
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an opencurlybracket
        elif self.current_character == "{":
            symbol.type = self.OPENCURLYBRACKET
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an closedcurlybracket
        elif self.current_character == "}":
            symbol.type = self.CLOSEDCURLYBRACKET
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is the end of file
        elif self.current_character == "":
            symbol.type = self.EOF
            #symbol.line = 
            #symbol.pos = 
            self.advance()

        #if symbol is an invalid character
        else:
            self.advance()

        return symbol