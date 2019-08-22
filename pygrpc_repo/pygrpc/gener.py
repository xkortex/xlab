#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

if __name__ == '__main__':

    delay = 1
    if len(sys.argv) > 1:
        delay = float(sys.argv[1])
    for i in range(5):
        print(i, flush=True)
        time.sleep(delay)
    print('quit', flush=True)
