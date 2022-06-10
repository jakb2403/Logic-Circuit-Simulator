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
    """Parser test for invalid name."""
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
    """Parser test for having a device type as a device name."""
    parser = dummy_parser(str(Path("test_files/parser_test2.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    NOR = NOR(2);\n"
        + "       ^\n"
        + "device type 'NOR' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_in_set_as_name(capfd):
    """Parser test for having a dtype input SET as a name."""
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


def test_parser_dtype_in_clear_as_name(capfd):
    """Parser test for having a dtype input CLEAR as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test4.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 9\n"
        + "    CLEAR = XOR;\n"
        + "         ^\n"
        + "dtype input/output 'CLEAR' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_in_data_as_name(capfd):
    """Parser test for having a dtype input DATA as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test5.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    DATA = NOR(2);\n"
        + "        ^\n"
        + "dtype input/output 'DATA' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_in_clk_as_name(capfd):
    """Parser test for having a dtype input CLK as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test6.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 4\n"
        + "    CLK = CLOCK(1);\n"
        + "       ^\n"
        + "dtype input/output 'CLK' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_out_q_as_name(capfd):
    """Parser test for having a dtype output Q as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test7.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 7\n"
        + "    Q = NAND(2);\n"
        + "     ^\n"
        + "dtype input/output 'Q' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_dtype_out_qbar_as_name(capfd):
    """Parser test for having a dtype output QBAR as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test8.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    QBAR = NOR(2);\n"
        + "        ^\n"
        + "dtype input/output 'QBAR' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_keyword_devices_as_name(capfd):
    """Parser test for having the keyword DEVICES as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test9.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    DEVICES = NOR(2);\n"
        + "           ^\n"
        + "keyword 'DEVICES' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_keyword_connect_as_name(capfd):
    """Parser test for having the keyword CONNECT as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test10.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_keyword_monitor_as_name(capfd):
    """Parser test for having the keyword MONITOR as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test11.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_keyword_end_as_name(capfd):
    """Parser test for having the keyword END as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test12.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_keyword_i_as_name(capfd):
    """Parser test for having the keyword I as a name."""
    parser = dummy_parser(str(Path("test_files/parser_test13.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    I = NOR(2);\n"
        + "     ^\n"
        + "keyword 'I' cannot be device name\n\n"
        + "Error Count: 1\n"
    )


def test_parser_keyword_invalid_argument_type_letter(capfd):
    """Parser test for having an invalid argument type of a letter"""
    parser = dummy_parser(str(Path("test_files/parser_test14.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 7\n"
        + "    NAND1 = NAND(d);\n"
        + "                  ^\n"
        + "invalid argument type\n\n"
        + "Error Count: 1\n"
    )


def test_parser_invalid_port_identifier(capfd):
    """Parser test for having an invalid port identifier."""
    #currently test file has no implanted errors
    parser = dummy_parser(str(Path("test_files/parser_test15.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_keyword_missing_symbol_equals(capfd):
    """Parser test for having a missing equals symbol."""
    parser = dummy_parser(str(Path("test_files/parser_test16.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 3\n"
        + "    SW4, SW5 SWITCH(0);\n"
        + "                   ^\n"
        + "missing symbol: =\n\n"
        + "Error Count: 1\n"
    )


def test_parser_keyword_missing_symbol_connection(capfd):
    """Parser test for having a missing connection symbol, >."""
    parser = dummy_parser(str(Path("test_files/parser_test17.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_keyword_missing_argument(capfd):
    """Parser test for having a missing argument."""
    parser = dummy_parser(str(Path("test_files/parser_test18.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_unrecognised_device_type(capfd):
    """Parser test for an unrecognised device type (with valid input syntax)."""
    parser = dummy_parser(str(Path("test_files/parser_test19.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 7\n"
        + "    NAND1 = RANDOM(2);\n"
        + "                  ^\n"
        + "unrecognised device type\n\n"
        + "Error Count: 1\n"
    )


def test_parser_missing_keyword1(capfd):
    """Parser test for a missing keyword DEVICES."""
    parser = dummy_parser(str(Path("test_files/parser_test20.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out ==  "Error on line 1\n"
                + "    SW1, SW2, SW3 = SWITCH(1);\n"
                + "      ^\n"
                + "missing keyword 'DEVICES'\n"
                + "\n"
                + "Error on line 1\n"
                + "    SW1, SW2, SW3 = SWITCH(1);\n"
                + "        ^\n"
                + "invalid device name\n"
                + "\n"
                + "Error Count: 2\n"
    )


def test_parser_argument_outside_array(capfd):
    """Parser test for a gate argument > 16."""
    parser = dummy_parser(str(Path("test_files/parser_test21.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 6\n"
        + "    OR1, OR2 = OR(50);\n"
        + "                     ^\n"
        + "argument '50' outside of accepted range\n\n"
        + "Error Count: 1\n"
    )


def test_parser_duplicate_name(capfd):
    """Parser test for a duplicate name."""
    parser = dummy_parser(str(Path("test_files/parser_test22.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 8\n"
        + "    NAND1 = NOR(2);\n"
        + "                  ^\n"
        + "name 'NAND1' already used in previous device assignment\n\n"
        + "Error Count: 1\n"
    )


def test_parser_duplicate_monitor(capfd):
    """Parser test for a duplicate monitor."""
    parser = dummy_parser(str(Path("test_files/parser_test23.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 33\n"
        + "    NOT1;\n"
        + "        ^\n"
        + "monitor point 'NOT1' already declared\n\n"
        + "Error Count: 1\n"
    )


def test_parser_monitor_an_input(capfd):
    """Parser test for monitoring an input."""
    parser = dummy_parser(str(Path("test_files/parser_test24.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
        == "Error on line 33\n"
        + "    OR2.I2;\n"
        + "          ^\n"
        + "monitor point is an input, only outputs are allowed\n\n"
        + "Error Count: 1\n"
    )


def test_parser_input_to_input(capfd):
    """Parser test for connecting an input to an input."""
    parser = dummy_parser(str(Path("test_files/parser_test25.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_output_to_output(capfd):
    """Parser test for connecting an output to an output."""
    parser = dummy_parser(str(Path("test_files/parser_test26.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_absent_port(capfd):
    """Parser test for absent port."""
    parser = dummy_parser(str(Path("test_files/parser_test27.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_input_already_in_use(capfd):
    """Parser test for an input already in use."""
    parser = dummy_parser(str(Path("test_files/parser_test28.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_incomplete_network(capfd):
    """Parser test for an incomplete network."""
    parser = dummy_parser(str(Path("test_files/parser_test29.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )


def test_parser_incorrect_section_ordering(capfd):
    """Parser test for incorrect section ordering."""
    parser = dummy_parser(str(Path("test_files/parser_test30.txt")))
    assert parser.parse_network() is False
    out, _ = capfd.readouterr()
    assert (
        out
    )