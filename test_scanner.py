import pytest
from pathlib import Path

from names import Names
from scanner import Scanner


def new_scanner(path):
    """Return a new instance of the Scanner class."""
    new_names = Names()
    new_scanner = Scanner(path, new_names)
    return new_scanner


def test_scanner1():
    """Test if get_symbol returns the correct symbol_id and
       symbol_type for scanner_test1.txt.
       scanner_test1.txt contains all possible symbols (some examples of
       numbers and names).
    """
    test_scanner1 = new_scanner(str(Path("test_files/scanner_test1.txt")))

    names = test_scanner1.names

    [G1_ID, G2_ID, G3_ID] = names.lookup(
        ["G1", "G2", "G3"]
    )

    expected_symbol_type_id = [
        (test_scanner1.DOT, None),
        (test_scanner1.COMMA, None),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.EQUALS, None),
        (test_scanner1.ARROW, None),
        (test_scanner1.OPENBRACKET, None),
        (test_scanner1.CLOSEDBRACKET, None),
        (test_scanner1.KEYWORD, test_scanner1.DEVICES_ID),
        (test_scanner1.KEYWORD, test_scanner1.CONNECT_ID),
        (test_scanner1.KEYWORD, test_scanner1.MONITOR_ID),
        (test_scanner1.KEYWORD, test_scanner1.END_ID),
        (test_scanner1.KEYWORD, test_scanner1.I_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.CLOCK_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.AND_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.NAND_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.OR_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.NOR_ID),
        (test_scanner1.DEVICE_ARG, test_scanner1.SWITCH_ID),
        (test_scanner1.DEVICE, test_scanner1.DTYPE_ID),
        (test_scanner1.DEVICE, test_scanner1.XOR_ID),
        (test_scanner1.DEVICE, test_scanner1.NOT_ID),
        (test_scanner1.DTYPE_IP, test_scanner1.SET_ID),
        (test_scanner1.DTYPE_IP, test_scanner1.CLEAR_ID),
        (test_scanner1.DTYPE_IP, test_scanner1.DATA_ID),
        (test_scanner1.DTYPE_IP, test_scanner1.CLK_ID),
        (test_scanner1.DTYPE_OP, test_scanner1.Q_ID),
        (test_scanner1.DTYPE_OP, test_scanner1.QBAR_ID),
        (test_scanner1.NUMBER, '1'),
        (test_scanner1.NUMBER, '2'),
        (test_scanner1.NUMBER, '3'),
        (test_scanner1.NUMBER, '4'),
        (test_scanner1.NUMBER, '5'),
        (test_scanner1.NAME, G1_ID),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.NAME, G3_ID),
        (test_scanner1.EOF, None)
    ]

    for i in range(len(expected_symbol_type_id)):
        symbol = test_scanner1.get_symbol()
        assert symbol.type == expected_symbol_type_id[i][0]
        assert symbol.id == expected_symbol_type_id[i][1]


def test_scanner2():
    """Test if get_symbol skips comments."""
    test_scanner2 = new_scanner(str(Path("test_files/scanner_test2.txt")))

    expected_symbol_type_id = [
        (test_scanner2.KEYWORD, test_scanner2.DEVICES_ID),
        (test_scanner2.EOF, None)
    ]

    for i in range(len(expected_symbol_type_id)):
        symbol = test_scanner2.get_symbol()
        assert symbol.type == expected_symbol_type_id[i][0]
        assert symbol.id == expected_symbol_type_id[i][1]


def test_scanner3():
    """Test if get_symbol correctly gets EOF symbol."""
    test_scanner3 = new_scanner(str(Path("test_files/scanner_test3.txt")))

    symbol = test_scanner3.get_symbol()
    assert symbol.type == test_scanner3.EOF
    assert symbol.id is None


def test_scanner4():
    """Test if get_symbol skips all unregistered symbols."""
    test_scanner4 = new_scanner(str(Path("test_files/scanner_test4.txt")))

    symbol = test_scanner4.get_symbol()

    assert symbol.type is None
    assert symbol.id is None


"""Test for scanner_test5.txt is in test_parser.py, which tests if error_found
   returns the correct error message, line and character numbers."""
