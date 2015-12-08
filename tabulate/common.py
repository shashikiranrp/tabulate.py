#!/usr/bin/python

#
# common utils for tabulate
#


import sys

LOG_ENABLE = True

def log_msg(msg):
  if LOG_ENABLE:
    sys.stderr.write(str(msg) + "\n")
