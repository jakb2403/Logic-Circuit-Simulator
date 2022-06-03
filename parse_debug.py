import os
from names import Names
from parse import Parser
from scanner import Scanner
from devices import Devices
from network import Network
from monitors import Monitors

path = os.getcwd() + "/test_parser1.txt"
print(path)
new_names = Names()
new_scanner = Scanner(path, new_names)
new_devices = Devices(new_names)
new_network = Network(new_names, new_devices)
new_monitors = Monitors(new_names, new_devices, new_network)
new_parser = Parser(new_names, new_devices, new_network, new_monitors, new_scanner)

new_parser.symbol = new_parser.scanner.get_symbol()
# new_parser.signal_name()
# new_parser.names()
# new_parser.assignment()
new_parser.section_devices()
print([(device.device_id, device.device_kind, device.inputs, device.outputs) for device in new_devices.devices_list])
new_parser.connection()


