# GF2 Logic Simulator Project 
## About
This repository contains Logic Simulator for Part IIA Engineering Project in Software Engineering (GF2) for Easter Term 2022. 

## Installation 
- Python version: 3.9.12
- All other requirements can be installed using `pip install -r requirements.txt`

## Logic Definition
This software is written to run logic circuits defined in a Logic Definition Language written by us. You can find some sample logic definition files [here](logic_definition) along with their circuit representations in `.png` format. The Extended Backus–Naur Form (EBNF) of our LDL grammar can be found [here](logic_definition/logic_definition_file.txt).

## Usage
- **To run the GUI** : typing `python logsim.py` into the terminal will open file opening dialogue box, from where you can choose a `.txt` to run. 
- **To run in the terminal** : typing `python logsim.py <.txt file>` will open a command line interface to run the simulator natively in the command line. To get help in this mode, type `h`.

## French Version
This software also comes with the ability to run the software in French on Linux. This functionality works in both the terminal interface and the GUI:
- **To run the GUI in French** : typing `LANG=fr_FR.utf8 .\logsim.py` will launch the GUI in French.
- **To run in the terminal in French** : typing `LANG=fr_FR.utf8 .\logsim.py -c <.txt file>` will run the terminal interface in French. 

## Acknowledgements
This software was written (in part) by team 15 in GF2P3 in Easter term 2022. The group members are Hyun Seung Cho, Joseph Waters and John Brown.
