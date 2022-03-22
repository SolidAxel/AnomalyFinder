from distutils.command.config import config
import json
from unittest import result
import drain3
import logging
import os
import subprocess
import sys
import time

from os.path import dirname
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,format='%(message)s')

fileHandler = logging.FileHandler('Output.log')
fileHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)

inLogFile = "03-08-22_152132__all.log"
if not os.path.isfile(inLogFile):
    logger.info('Make sure file is in same directory as this program.')
    Exception('File not found in current directory.')

config = TemplateMinerConfig()
config.profiling_enabled = True
template_miner = TemplateMiner(config=config)

lineCount = 0

with open(inLogFile) as f:
    lines = f.readlines()

startTime = time.time()
procStartTime = startTime
procSize = 10000

for line in lines:
    line = line.rstrip()
    line = line.partition(']')[2]
    result = template_miner.add_log_message(line)
    lineCount += 1
    if lineCount % procSize == 0:
        timeTaken = time.time() - procStartTime
        rate = procSize / timeTaken
        logger.info(f"Processing line: {lineCount}, rate {rate:.1f} lines/sec, " f"{len(template_miner.drain.clusters)} clusters so far.")
        procStartTime = time.time()
    if result["change_type"] != "none":
        resultJSON = json.dumps(result)
        logger.info(f"Input ({lineCount}): " + line)
        logger.info("Result: " + resultJSON)
        


timeTaken = time.time() - startTime
rate = lineCount / timeTaken
logger.info(f"--- Done processing file in {timeTaken:.2f} sec. Total of {lineCount} lines, rate {rate:.1f} lines/sec, " f"{len(template_miner.drain.clusters)} clusters")
sortedClusters = sorted(template_miner.drain.clusters, key=lambda it: it.size, reverse=True)
for cluster in sortedClusters:
    logger.info(cluster)
print("Prefix Tree:")
template_miner.drain.print_tree()
template_miner.profiler.report(0)