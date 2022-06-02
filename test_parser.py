import pytest
import os
from names import Names
from parse2 import Parser
from scanner import Scanner
from devices import Devices
from network import Network
from monitors import Monitors

def new_parser(path):
    """Return a new parser instance."""
    new_names = Names()
    new_scanner = Scanner(path, new_names)
    new_devices = Devices(new_names)
    new_network = Network(new_names, new_devices)
    new_monitors = Monitors(new_names, new_devices, new_network)
    new_parser = Parser(new_names, new_devices, new_network, new_monitors, new_scanner)
    return new_parser

def test_parser1():
    path1 = os.getcwd() + "\\test_scanner1.txt"
    test_parser1 = new_parser(path1)
    assert test_parser1.parse_network() == True