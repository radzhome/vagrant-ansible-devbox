#!/usr/bin/env python
"""
Changes the filename by adding a timestamp
"""

# This file is managed by Ansible. Local changes will be lost!

import os
import shutil
import sys
import time

FULL_FILENAME = sys.argv[1]
SPLIT_FILENAME = os.path.split(FULL_FILENAME)

# Format params timestamp, base filename path (parent)
DEST_FILENAME = "{}_{}_{}".format(SPLIT_FILENAME[0].split('/')[-1], str(int(time.time())), SPLIT_FILENAME[1])

FULL_DESTINATION = "{}/{}".format(SPLIT_FILENAME[0], DEST_FILENAME)
shutil.move(FULL_FILENAME, FULL_DESTINATION)
print FULL_DESTINATION
