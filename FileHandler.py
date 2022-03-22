from distutils.command.config import config
import json
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

inLogFile = sys.stdin
if not os.path.isfile(inLogFile):
    logger.info('Make sure file is in same directory as this program.')
    Exception('File not found in current directory.')

config = TemplateMinerConfig()
config.profiling_enabled = True
template_miner = TemplateMiner(config=config)

lineCount = 0

with open(inLogFile) as f:
    lines = f.readlines()

