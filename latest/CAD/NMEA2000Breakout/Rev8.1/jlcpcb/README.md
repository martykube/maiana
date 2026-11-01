# JLCPCB production files: NMEA 2000 adapter 8.1

Generated from the KiCad project in the parent directory with `kicad-cli` (KiCad 9).
Copper and drills match the original Gerbers in `../Gerbers/`.

| File | Upload as |
|---|---|
| `nmea2000-adapter-8.1-gerbers-JLCPCB.zip` | Gerber file |
| `nmea2000-adapter-8.1-BOM-JLCPCB.csv` | BOM |
| `nmea2000-adapter-8.1-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 2 layers, **1.6 mm**, 46.1 x 46.1 mm
- Order number: "Specify a location" (the board has a `JLCJLCJLCJLC` marker)
- PCB assembly: J2 (RJ45) is on the **bottom** side; everything else SMT is on top.
  Either choose both-sides assembly, or assemble top only and hand-solder J2.

## Parts

LCSC numbers are stored in the `LCSC` field of each schematic symbol.

Changes from the original design:

| Ref | Original | Fitted | Why |
|---|---|---|---|
| J2 | RJ-82A86MMNL | FG RJ-055-1 (C7205195) | Sunken SMD RJ45; same footprint as the transponder board |
| U6 | ISO7721FDR (schematic) / ISO7721DR (PCB) | ISO7721DR (C366164) | Output defaults high when USB is unplugged, so the transponder's RX idles instead of seeing a break |
| SW1, SW2 | CL-SB-12B-01T | CL-SB-12B-01 (C5619703) | Same switch, non-tape packaging (01T out of stock) |
| D5 | PESD1CAN-U | PESD1CAN-UX (C152727) | Nexperia SOT-323 orderable part number |
| D8 | generic Schottky | B5819W (C8598) | 40 V 1 A, SOD-123, basic part |
| D1-D4 | LED (no colour) | green KT-1206G (C14641) | Colour not specified in the design |

### Not assembled by JLCPCB

| Ref | Part | Notes |
|---|---|---|
| J1 | 12-3701-05 M12 5-pin (NMEA 2000 Micro-C), THT | Not stocked at JLCPCB; hand-solder |
| J4 | 2-pin header | DNP in the design |

## Rotations

The CPL rotations have been corrected for JLCPCB's part models (checked in the JLCPCB placement
preview, Nov 2026): SOIC/SO/TSSOP/SOT-23-6/SOT-323 parts (U2-U6, D5) are -90 deg from KiCad,
SOT-23/SOT-23-5 parts (Q1-Q3, U7, U8) and the bottom-side RJ45 (J2) are 180 deg from KiCad.
Do not regenerate the CPL from KiCad without re-applying these.
