#!/usr/bin/env python3
"""
Copyright 2019 Dean Hall.  See LICENSE for details.

Lorp - the LoRa Point to Point Protocol
a Data Link Layer (Layer 2) protocol for LoRa radio modems.
"""

import farc  # pip install farc

from sx127x_ahsm import SX127xSpiAhsm


class LorpAhsm(farc.Ahsm):
    """State machine that manages the Lorp point-to-point protocol
    """

    @farc.Hsm.state
    def initial(me, event):
        """Pseudostate: LorpAhsm:initial
        """
        farc.Signal.register("_TBD")

        return me.tran(me, LorpAhsm.initializing)


    @farc.Hsm.state
    def initializing(me, event):
        """State: LorpAhsm:initializing
        """
        sig = event.signal
        if sig == farc.Signal.ENTRY:
            pass

        return me.super(me, me.top)


    @farc.Hsm.state
    def idling(me, event):
        """State: LorpAhsm:idling
        """
        sig = event.signal
        if sig == farc.Signal.ENTRY:
            return me.handled(me, event)

        return me.super(me, me.top)


    @farc.Hsm.state
    def negotiating(me, event):
        """State: LorpAhsm:negotiating
        """
        sig = event.signal
        if sig == farc.Signal.ENTRY:
            return me.handled(me, event)

        return me.super(me, me.top)


    @farc.Hsm.state
    def networking(me, event):
        """State: LorpAhsm:networking
        """
        sig = event.signal
        if sig == farc.Signal.ENTRY:
            return me.handled(me, event)

        return me.super(me, me.top)


    @farc.Hsm.state
    def terminating(me, event):
        """State: LorpAhsm:terminating
        """
        sig = event.signal
        if sig == farc.Signal.ENTRY:
            return me.handled(me, event)

        return me.super(me, me.top)
