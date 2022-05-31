"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from inspect import FrameInfo, currentframe, getframeinfo
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

        self.char_counter = 0

        self.path = os.path.basename(path)

        self.file = open(self.path, 'r')
        self.lines = len(self.file.readlines())
        print("number of lines in this file: ", self.lines)


        self.names = names
        self.symbol_type_list = [
            self.DOT,
            self.COMMA,
            self.SEMICOLON,
            self.EQUALS,
            self.ARROW,
            self.NEXTLINE,
            self.HASHTAG,
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
            self.EOF] = range(19)  
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
        self.char_counter += 1 #add 1 to the character counter to track location in line
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
        line_number = currentframe().f_back.f_lineno #find the line
        char_number = self.char_counter #find the character
        newline = "\n" + (self.char_counter - 1)*" " + "^" + "\n" #format the newline with ^ below the error
        error_line = "\n" + "***Error detected***"
        output = self.path.readline() + newline + error_line #insert new empty line below 
        return output  

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.current_character = self.skip_spaces()

        #if symbol is a name
        if self.current_character.isalpha():
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
                [symbol.id] = self.names.lookup([name_string])

        #if symbol is a number
        elif self.current_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        #if symbol is a dot
        elif self.current_character == ".":
            symbol.type = self.DOT
            self.get_next_character()

        #if symbol is a comma
        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.get_next_character()    

        #if symbol is a semicolon
        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            self.get_next_character()

        #if symbol is a equals
        elif self.current_character == "=":
            symbol.type = self.EQUALS
            self.get_next_character()

        #if symbol is an arrow
        elif self.current_character == "->":
            symbol.type = self.ARROW
            self.get_next_character()

        #if symbol is a nextline
        elif self.current_character == "\n":
            symbol.type = self.NEXTLINE
            self.get_next_character()

        #if symbol is a hashtag
        elif self.current_character == "#":
            symbol.type = self.HASHTAG
            self.file.next()
            self.get_next_character()

        #if symbol is an openbracket
        elif self.current_character == "(":
            symbol.type = self.OPENBRACKET
            self.get_next_character()

        #if symbol is an closedbracket
        elif self.current_character == ")":
            symbol.type = self.CLOSEDBRACKET
            self.get_next_character()

        #if symbol is an opencurlybracket
        elif self.current_character == "{":
            symbol.type = self.OPENCURLYBRACKET
            self.get_next_character()

        #if symbol is an closedcurlybracket
        elif self.current_character == "}":
            symbol.type = self.CLOSEDCURLYBRACKET
            self.get_next_character()

        #if symbol is the end of file
        elif self.current_character == "":
            symbol.type = self.EOF
            self.get_next_character()

        #if symbol is an invalid character
        else:
            self.get_next_character()

        return symbol