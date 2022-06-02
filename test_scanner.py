import pytest
import os

from names import Names
from scanner import Scanner


def new_scanner(path):
    """Return a new instance of the Scanner class."""
    new_names = Names()
    new_scanner = Scanner(path, new_names)
    return new_scanner


def test_scanner1():
    """Test if get_symbol returns the correct symbol_id and
        symbol_type for test_scanner1.txt"""
    path1 = os.getcwd() + "\\test_scanner1.txt"
    test_scanner1 = new_scanner(path1)
    names = test_scanner1.names

    [SW1_ID, SW2_ID, G1_ID, IN1_ID, G2_ID] = names.lookup(
        ["SW1", "SW2", "G1", "IN1", "G2"]
    )
    expected_symbol_type_id = [
        (test_scanner1.KEYWORD, test_scanner1.DEVICES_ID),
        (test_scanner1.OPENCURLYBRACKET, None),
        (test_scanner1.NAME, SW1_ID),
        (test_scanner1.COMMA, None),
        (test_scanner1.NAME, SW2_ID),
        (test_scanner1.EQUALS, None),
        (test_scanner1.DEVICE_ARG, test_scanner1.SWITCH_ID),
        (test_scanner1.OPENBRACKET, None),
        (test_scanner1.NUMBER, '0'),
        (test_scanner1.CLOSEDBRACKET, None),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, G1_ID),
        (test_scanner1.EQUALS, None),
        (test_scanner1.DEVICE_ARG, test_scanner1.NAND_ID),
        (test_scanner1.OPENBRACKET, None),
        (test_scanner1.NUMBER, '2'),
        (test_scanner1.CLOSEDBRACKET, None),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, IN1_ID),
        (test_scanner1.EQUALS, None),
        (test_scanner1.DEVICE_ARG, test_scanner1.CLOCK_ID),
        (test_scanner1.OPENBRACKET, None),
        (test_scanner1.NUMBER, '50'),
        (test_scanner1.CLOSEDBRACKET, None),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.EQUALS, None),
        (test_scanner1.DEVICE, test_scanner1.DTYPE_ID),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.CLOSEDCURLYBRACKET, None),
        (test_scanner1.KEYWORD, test_scanner1.CONNECT_ID),
        (test_scanner1.OPENCURLYBRACKET, None),
        (test_scanner1.NAME, SW1_ID),
        (test_scanner1.ARROW, None),
        (test_scanner1.NAME, G1_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.KEYWORD, test_scanner1.I_ID),
        (test_scanner1.NUMBER, '1'),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, SW2_ID),
        (test_scanner1.ARROW, None),
        (test_scanner1.NAME, G1_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.KEYWORD, test_scanner1.I_ID),
        (test_scanner1.NUMBER, '2'),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, G1_ID),
        (test_scanner1.ARROW, None),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.DTYPE_IP, test_scanner1.DATA_ID),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, IN1_ID),
        (test_scanner1.ARROW, None),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.DTYPE_IP, test_scanner1.CLK_ID),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.CLOSEDCURLYBRACKET, None),
        (test_scanner1.KEYWORD, test_scanner1.MONITOR_ID),
        (test_scanner1.OPENCURLYBRACKET, None),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.DTYPE_OP, test_scanner1.Q_ID),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.NAME, G2_ID),
        (test_scanner1.DOT, None),
        (test_scanner1.DTYPE_OP, test_scanner1.QBAR_ID),
        (test_scanner1.SEMICOLON, None),
        (test_scanner1.CLOSEDCURLYBRACKET, None),
        (test_scanner1.EOF, None)
    ]
    print(expected_symbol_type_id)
    
    for i in range(len(expected_symbol_type_id)):
        symbol = test_scanner1.get_symbol()
        print(symbol.type, symbol.id, i)
        assert symbol.type == expected_symbol_type_id[i][0]
        assert symbol.id == expected_symbol_type_id[i][1]
        
