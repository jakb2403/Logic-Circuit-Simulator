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


@pytest.mark.parametrize("path", [
    "test_files/parser_test_1.txt",
    "test_files/parser_test_2.txt"
])
def test_parser1(path):
    """Tests if the parser returns True for correct definition files"""
    parser = dummy_parser(str(Path(path)))
    assert parser.parse_network is True


def test_parser2(capfd):
    """whatever we test for"""
    parser = dummy_parser(str(Path("test_files/parser_test2.txt")))
    assert parser.parse_network is False  # NEEDS CHANGING!!!
    out, _ = capfd.readouterr()
    assert (
        out
        == "\n    2g = NAND(2),"
        + "     ^"
        + "SyntaxError: invalid device name"
    )