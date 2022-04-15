# AnomalyFinder
Attempts to find anomolies in logs.
## Required packages:
---
* pip install drain3
## Use
---
Use of this program is pretty simple at the moment. In order to run the program, you need to:
* Open a terminal or command prompt and navigate to the path in which the program is located.
* Run the command python parseTrainer.py or python3 parseTrainer.py
* The program will then ask for an input log file, which it will then parse when the enter key is pressed.
* The program will also ask for an output log file. This file can either be an existing one that will be overwritten or a new one that will be created by the program. (The program will also output the results to the terminal or command prompt.) 

This program also creates a binary file which holds the program's state. This is to ensure that what the program has learned through training isn't lost after each use or lost because of an interruption during parsing. 

## TODO
---
* Automatically find anomalies in the parsed logs
* Fully train parsing model