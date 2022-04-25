from distutils.command.config import config
import json
from posixpath import abspath
from unittest import result
import logging
import os
import sys
import time

from os.path import dirname
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.file_persistence import FilePersistence
from requests import get

persistence = FilePersistence("states/drain3State.bin")

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(message)s"
)

fileHandler = logging.FileHandler("Output.log")
fileHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)

inLogFile = input("Please enter filename>> ")
if not os.path.isfile(inLogFile):
    logger.info("Make sure file is in same directory as this program.")
    Exception("File not found in current directory.")

config = TemplateMinerConfig()
config.load(dirname(os.path.abspath(__file__)) + "/drainConfig.ini")
config.profiling_enabled = True
templateMiner = TemplateMiner(persistence, config=config)

lineCount = 0

with open(inLogFile) as f:
    lines = f.readlines()

startTime = time.time()
procStartTime = startTime
procSize = 10000
params = []

for line in lines:
    line = line.rstrip()
    line = line.partition("] ")[2]
    result = templateMiner.add_log_message(line)
    parameters = templateMiner.extract_parameters(
        result["template_mined"], line, exact_matching=True
    )
    if parameters:
        params.append(parameters)
    lineCount += 1
    if lineCount % procSize == 0:
        timeTaken = time.time() - procStartTime
        rate = procSize / timeTaken
        logger.info(
            f"Processing line: {lineCount}, rate {rate:.1f} lines/sec, "
            f"{len(templateMiner.drain.clusters)} clusters so far."
        )
        procStartTime = time.time()
    if result["change_type"] != "none":
        resultJSON = json.dumps(result)
        logger.info(f"Input ({lineCount}): " + line)
        logger.info("Result: " + resultJSON)


timeTaken = time.time() - startTime
rate = lineCount / timeTaken
logger.info(
    f"--- Done processing file in {timeTaken:.2f} sec. Total of {lineCount} lines, rate {rate:.1f} lines/sec, "
    f"{len(templateMiner.drain.clusters)} clusters"
)
sortedClusters = sorted(
    templateMiner.drain.clusters, key=lambda it: it.size, reverse=True
)
for cluster in sortedClusters:
    logger.info(cluster)
print("Prefix Tree:")
templateMiner.drain.print_tree()
templateMiner.profiler.report(0)
# TODO Move this to it's own seperate .py
bat = None
boot = None
for x in params:
    for y in x:
        if getattr(y, "mask_name") == "BAT_VOL":
            bat = getattr(y, "value").split(" ")[1]
        elif getattr(y, "mask_name") == "BOOT_TYPE":
            # boot = getattr(y, "value").split()
            boot = getattr(y, "value").split("=")[1]

if boot == "WarmBoot":
    assert int(bat) >= 1.5
elif boot == "ColdBoot":
    assert int(bat) < 1.5
# print(str(params))
