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
    "test_files/parser_test_1.txt"
])
def test_parser_returns_true(path):
    """Tests if the parser returns True for correct definition files"""
    parser = dummy_parser(str(Path(path)))
    assert parser.parse_network() is True
