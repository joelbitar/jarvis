#!/usr/bin/env python
import argparse
import time

import tellcore.telldus as td
import tellcore.constants as const

core = td.TelldusCore()

for d in core.devices():
    if d.id == 1:
        d.learn()
