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

A Lorp frame contains just these fields:

    { Protocol, Data }

Lorp is able to do-away with most of the fields from PPP:

    { Flag, Address, Control, Protocol, Data, FCS, Flag }.

The Address, Control and two Flag fields are constant values.
Lorp elides most of the PPP fields because they are not necessary on LoRa links.
Instead, Lorp relies on either the LoRa physical layer to provide a CRC-16,
or a higher layer to provide a trailing FCS or MIC more robust than a CRC-16.
The Protocol field identifies the type of information in the Data field of the frame.
Since space is at a premium inside a LoRa packet, the Protocol field is reduced to one octet.
Bit stuffing is not used in Lorp.


## Protocols

The following table defines the Protocol ID (PID) value(s) used to identify
the protocol used in the subsequent data.  Ranges of values are used in some
cases to allow the Most Significant Bits (MSb) to select the protocol
and the remaining bits to be used for some other protocol-specific purpose
(such as versioning or bit-flag options).

| PID (dec)  | PID (hex)  | Protocol |
| ---------- | ---------- | -------- |
| 0, 1       | 0x00, 0x01 | Raw data, control |
| 2, 3       | 0x02, 0x03 | [Link Control Protocol data, control](https://tools.ietf.org/html/rfc1661) |
| 4..192     | 0x04..0xC0 | RFU      |
| 193        | 0xC1       | [MessagePack](https://msgpack.org/index.html) |
| 194, 195   | 0xC2, 0xC3 | [Codec2 data, ctrl](http://www.rowetel.com/wordpress/?page_id=452) |
| 196..219   | 0xC4..0xDB | RFU      |
| 220..223   | 0xDC..0xDF | [Experimental/Test use](https://tools.ietf.org/html/rfc3692) only |
| 224..255   | 0xE0..0xFF | [HeyMac and HeyMacFlood](https://github.com/dwhall/HeyMac) |

Rationale:

- In MessagePack, the value 0xC1 is the only bit pattern that is "Never Used".
- "C2" is a good shorthand/moniker for Codec2.
- In HeyMac, the range 0xEX is used in HeyMac's PID_Ver field
    (the first byte of the HeyMac frame).  So HeyMac and Lorp can coexist
    through superposition (HeyMac frame's PID_Ver field satisfies Lorp's
    Protocol octet).

No protocols are implemented yet.
Here is a list of other potential protocols to support:

- LCP Control
- LCP Data
- UTF-8 text
- APRS
- Codec2 (in some frame-delimiting wrapper)


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

