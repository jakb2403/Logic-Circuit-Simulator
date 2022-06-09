import pytest
import os
from pathlib import Path

from names import Names
from parse import Parser
from scanner import Scanner
from devices import Devices
from network import Network
from monitors import Monitors


def dummy_parser(path):
    """Return a new parser instance."""
    new_names = Names()
    new_scanner = Scanner(path, new_names)
    new_devices = Devices(new_names)
    new_network = Network(new_names, new_devices)
    new_monitors = Monitors(new_names, new_devices, new_network)
    new_parser = Parser(new_names, new_devices, new_network,
                        new_monitors, new_scanner)
    return new_parser


# def test_scanner5():
#     """Test if error_found returns the correct error message, line and
#        character numbers."""
#     test_scanner5 = dummy_parser(
#         str(Path("test_files/scanner_test5.txt"))
#     )
#     out = test_scanner5.scanner.error_found()
#     assert out == "Error on line 1\n\n^"
#     assert test_scanner5.scanner.line_counter == 1
#     assert test_scanner5.scanner.char_counter == 1


def test_parser_invalid_name(capfd):
    """Parser test for invalid name"""
    parser = dummy_parser(str(Path("test_files/parser_names_test1.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 7\n"
        + "    2g = NAND(2);\n"
        + "     ^\n"
        + "invalid device name\n\n"
        + "Error Count: 1\n"
    )

######################################################################


def test_parser_input_with_number(capfd):
    """Parser test for argument with an input with a letter in it"""
    parser = dummy_parser(str(Path("test_files/parser_argument_test1.txt")))
    assert parser.parse_network is False  # NEEDS CHANGING!!!
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 6\n"
        + "    OR1, OR2 = OR(p);\n"
        + "                   ^\n"
        + "invalid argument type\n\n"
        + "Error Count: 1\n"        
    )
    #or gate has argumnet "p"


# def test_parser_input_without_number(capfd):
#     """Parser test for argument with an input without a number in it"""
#     parser = dummy_parser(str(Path("test_files/parser_argument_test2.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #nor gate has no argument


# def test_parser_input_with_multiple_numbers(capfd):
#     """Parser test for argument with an input with a number out of range"""
#     parser = dummy_parser(str(Path("test_files/parser_argument_test3.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #and gate has argument = 5

##############################################################################

# def test_parser_invalid_signal_name(capfd):
#     """Parser test for signal name with an invalid input"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test1.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #sw2 is now sw5


# def test_parser_invalid_dtype_input_set(capfd):
#     """Parser test for signal name with an invalid dtype input SET"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test2.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #SW1 > AND1.SET;


# def test_parser_invalid_dtype_input_clear(capfd):
#     """Parser test for signal name with an invalid dtype input CLEAR"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test3.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #SW1 > AND1.CLEAR;


# def test_parser_invalid_dtype_input_data(capfd):
#     """Parser test for signal name with an invalid dtype input DATA"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test4.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #SW1 > AND1.DATA;


# def test_parser_invalid_dtype_input_clk(capfd):
#     """Parser test for signal name with an invalid dtype input CLK"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test5.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert #SW1 > AND1.CLK;


# def test_parser_invalid_gate_name(capfd):
#     """Parser test for signal name with an invalid gate name"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test6.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert


# def test_parser_invalid_gate_and_output_name(capfd):
#     """Parser test for signal name with an invalid gate and output name"""
#     parser = dummy_parser(str(Path("test_files/parser_signalname_test7.txt")))
#     assert parser.parse_network is False  # NEEDS CHANGING!!!
#     out, _ = capfd.readouterr()
#     assert