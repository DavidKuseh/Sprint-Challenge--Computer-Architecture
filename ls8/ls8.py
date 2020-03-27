#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    sys.exit(1)

cpu = CPU()

cpu.load()
cpu.run()

