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


#####################################################################


# def test_parser_(capfd):
#     """Parser test for """
#     parser = dummy_parser(str(Path("test_files/parser_base_file.txt")))
#     assert parser.parse_network() is False
#     out, _ = capfd.readouterr()
#     assert (
#         out 
#     )

#####################################################################


def test_parser_invalid_name(capfd):
    """Parser test for invalid name"""
    parser = dummy_parser(str(Path("test_files/parser_test1.txt")))
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


def test_parser_dev_type_as_dev_name(capfd):
    """Parser test for having a device type as a device name"""
    parser = dummy_parser(str(Path("test_files/parser_test2.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out 
       == "Error on line 7\n"
        + "    NOR = NOR(2);\n"
        + "       ^\n"
        + "device type 'NOR' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_in_set_as_name(capfd):
    """Parser test for having a dtype input SET as a name"""
    parser = dummy_parser(str(Path("test_files/parser_test3.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out 
       == "Error on line 5\n"
        + "    AND1, SET = AND(2);\n"
        + "             ^\n"
        + "dtype input/output 'SET' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_in_clear__as_name(capfd):
    """Parser test for having a dtype input CLEAR as a name"""
    parser = dummy_parser(str(Path("test_files/parser_test4.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out 
       == "Error on line 5\n"
        + "    AND1, SET = AND(2);\n"
        + "             ^\n"
        + "dtype input/output 'SET' cannot be device name\n\n"
        + "Error Count: 1\n"
    )