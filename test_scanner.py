import pytest
import os

from names import Names
from scanner import Scanner


@pytest.fixture
def new_scanner():
    """Return a new instance of the Scanner class,
        which opens test_scanner1.txt."""
    new_names = Names()
    path = os.getcwd() + "\\test_scanner1.txt"
    new_scanner = Scanner(path, new_names)
    return new_scanner


def test_get_symbol(new_scanner):
    """Test if get_symbol returns the correct symbol type and id."""
    names = new_scanner.names

    [SW1_ID, SW2_ID, G1_ID, IN1_ID, G2_ID] = names.lookup(
        ["SW1", "SW2", "G1", "IN1", "G2"]
    )
    expected_symbol_type_id = [
        (new_scanner.KEYWORD, new_scanner.DEVICES_ID),
        (new_scanner.OPENCURLYBRACKET, None),
        (new_scanner.NAME, SW1_ID),
        (new_scanner.COMMA, None),
        (new_scanner.NAME, SW2_ID),
        (new_scanner.EQUALS, None),
        (new_scanner.DEVICE_ARG, new_scanner.SWITCH_ID),
        (new_scanner.OPENBRACKET, None),
        (new_scanner.NUMBER, '0'),
        (new_scanner.CLOSEDBRACKET, None),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, G1_ID),
        (new_scanner.EQUALS, None),
        (new_scanner.DEVICE_ARG, new_scanner.NAND_ID),
        (new_scanner.OPENBRACKET, None),
        (new_scanner.NUMBER, '2'),
        (new_scanner.CLOSEDBRACKET, None),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, IN1_ID),
        (new_scanner.EQUALS, None),
        (new_scanner.DEVICE_ARG, new_scanner.CLOCK_ID),
        (new_scanner.OPENBRACKET, None),
        (new_scanner.NUMBER, '50'),
        (new_scanner.CLOSEDBRACKET, None),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, G2_ID),
        (new_scanner.EQUALS, None),
        (new_scanner.DEVICE, new_scanner.DTYPE_ID),
        (new_scanner.SEMICOLON, None),
        (new_scanner.CLOSEDCURLYBRACKET, None),
        (new_scanner.KEYWORD, new_scanner.CONNECT_ID),
        (new_scanner.OPENCURLYBRACKET, None),
        (new_scanner.NAME, SW1_ID),
        (new_scanner.ARROW, None),
        (new_scanner.NAME, G1_ID),
        (new_scanner.DOT, None),
        (new_scanner.KEYWORD, new_scanner.I_ID),
        (new_scanner.NUMBER, '1'),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, SW2_ID),
        (new_scanner.ARROW, None),
        (new_scanner.NAME, G1_ID),
        (new_scanner.DOT, None),
        (new_scanner.KEYWORD, new_scanner.I_ID),
        (new_scanner.NUMBER, '2'),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, G1_ID),
        (new_scanner.ARROW, None),
        (new_scanner.NAME, G2_ID),
        (new_scanner.DOT, None),
        (new_scanner.DTYPE_IP, new_scanner.DATA_ID),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, IN1_ID),
        (new_scanner.ARROW, None),
        (new_scanner.NAME, G2_ID),
        (new_scanner.DOT, None),
        (new_scanner.DTYPE_IP, new_scanner.CLK_ID),
        (new_scanner.SEMICOLON, None),
        (new_scanner.CLOSEDCURLYBRACKET, None),
        (new_scanner.KEYWORD, new_scanner.MONITOR_ID),
        (new_scanner.OPENCURLYBRACKET, None),
        (new_scanner.NAME, G2_ID),
        (new_scanner.DOT, None),
        (new_scanner.DTYPE_OP, new_scanner.Q_ID),
        (new_scanner.SEMICOLON, None),
        (new_scanner.NAME, G2_ID),
        (new_scanner.DOT, None),
        (new_scanner.DTYPE_OP, new_scanner.QBAR_ID),
        (new_scanner.SEMICOLON, None),
        (new_scanner.CLOSEDCURLYBRACKET, None),
        (new_scanner.EOF, None)
    ]

    for i in range(len(expected_symbol_type_id)):
        symbol = new_scanner.get_symbol()
        assert symbol.type == expected_symbol_type_id[i][0]
        assert symbol.id == expected_symbol_type_id[i][1]
