from pathlib import Path
from names import Names
from parse import Parser
from scanner import Scanner
from devices import Devices
from network import Network
from monitors import Monitors

path = str(Path("test_parse1.txt"))

new_names = Names()
new_scanner = Scanner(path, new_names)
new_devices = Devices(new_names)
new_network = Network(new_names, new_devices)
new_monitors = Monitors(new_names, new_devices, new_network)
new_parser = Parser(new_names, new_devices, new_network, new_monitors,
                    new_scanner)
new_parser.symbol = new_parser.scanner.get_symbol()
new_parser._section_devices()
new_parser._section_connect()
