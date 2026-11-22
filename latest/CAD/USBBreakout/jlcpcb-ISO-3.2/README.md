# JLCPCB production files: USB breakout ISO 3.2 (DRAFT, not yet quoted)

Eagle design (`../USBBreakout-ISO-3.2.brd/.sch`). Gerbers are Peter's original CAM output; the CPL comes
from his pick-and-place files (front + back). The BOM was matched to LCSC numbers on 2026-11-18.

| File | Upload as |
|---|---|
| `usb-breakout-iso-3.2-gerbers-JLCPCB.zip` | Gerber file |
| `usb-breakout-iso-3.2-BOM-JLCPCB.csv` | BOM |
| `usb-breakout-iso-3.2-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 2 layers, 1.6 mm, 38 x 48 mm
- Packaged in Peter's `../USBBreakoutEnclosure-2.0.FCStd` box with the `../USBBreakoutFrontPanel-1.0` PCB lid

## Before ordering

- U1 pi122U31 (C471590) and the 2 slide switches CL-SB-12B-01T (C2921647) are 0 stock at JLC:
  pre-order them to My Parts Lib (min 31 and 17), as with the TB0436A.
- J2 (micro-USB, SMD) and J3 (sunken SMD RJ45) are on the BOTTOM side: order Standard PCBA,
  assemble both sides (decided 2026-11-18).
- J3 RJ-82A86MMNL -> FG RJ-055-1 (C7205195), the same substitute as the transponder 12.0.1 J4 and
  the NMEA 0183 7.1 J1 (pins, pegs, cutout and shield tabs match the footprint). Standard PCBA only.
- U1 and the switches were put in the JLC parts cart for pre-order on 2026-11-18.
- J1 (OSTVN02A150 terminal block, THT) is hand-soldered; DigiKey.
- Rotations are Peter's Eagle values, NOT yet checked in JLC's placement preview. On the UART 3.0,
  SOIC-8 / SOT-23 / SOT-23-6 parts needed -90 deg.
