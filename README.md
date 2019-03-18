# Lorp
LoRa Point to Point Protocol

Lorp is a distillation of [PPP](https://en.wikipedia.org/wiki/Point-to-Point_Protocol)
for [LoRa](https://en.wikipedia.org/wiki/LoRa) radio point-to-point links.
It allows LoRa endpoints to negotiate links, optionally mutually-authenticate and
pass various protocols while consuming as little as one octet of the LoRa frame.

This repository contains the proof-of-concept implementation of lorp.
It is written in Python3 using the [farc](https://github.com/dwhall/farc)
state machine framework.
The target platform is a RaspberryPi running Linux.

## Frame Format

For reference, a PPP frame contains the fields:

    { Flag, Address, Control, Protocol, Data, FCS, Flag }.

The Address, Control and two Flag fields are constant values.
Lorp elides most of the PPP fields because they are not necessary on LoRa links.
Instead, a Lorp frame contains just these fields:

    { Protocol, Data }

and relies on either the LoRa physical layer to provide a CRC-16, or a higher layer
to provide a trailing FCS or MIC more robust than a CRC-16.
The Protocol field identifies the type of information in the Data field of the frame.
Since space is at a premium inside a LoRa packet, the Protocol field is reduced to one octet.
Bit stuffing is used in PPP, but not in Lorp.

## Link Configuration

Lorp also distills the Link Control Protocol (LCP) and its link configuration semantics
that are a component of PPP and defined in [RFC 1661](https://tools.ietf.org/html/rfc1661).
The LCP carries packets for establishing, maintaining and ending Lorp links.

Lorp's LCP packet has the same fields as that in PPP:

    { Code, ID, Length, LCP Data }

However, Lorp uses [MessagePack](https://msgpack.org/index.html)
instead of Tag/Length/Value for structured data in the LCP Data field.
The following is a partial list of the LCP codes:

| Code Value | LCP Packet Type |
| ---------- | --------------- |
| 0x01       | Configure-request |
| 0x02       | Configure-ack |
| 0x03       | Configure-nak |
| 0x04       | Configure-reject |
| 0x07       | Code-reject |
| 0x08       | Protocol-reject |

## Link Initialization

Two LoRa endpoints must start with the same base configuration
in order to establish an initial link. From there, the two endpoints
use LCP to negotiate a better configuration.
The base configuration is a slow data rate to allow the greatest chance
at a successful initial link.  Higher data rates may be negotiated if
the link quality is indicative of potential success at the higher rate.
