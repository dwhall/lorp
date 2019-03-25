#!/usr/bin/env python3

"""
Copyright 2019 Dean Hall.  See LICENSE for details.

Launches all the state machines to run Lorp
"""


import asyncio

import lorp


def main():
    # Instantiate state machines
    lorpAhsm = lorp.LorpAhsm(lorp.LorpAhsm.initial)

    # Start state machines (with priorities)
    lorpAhsm.start(10)

    # Start event loop
    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()
