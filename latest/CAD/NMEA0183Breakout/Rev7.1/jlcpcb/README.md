# JLCPCB production files: NMEA 0183 adapter 7.1

Generated from the KiCad project in the parent directory with `kicad-cli` (KiCad 9).
Copper and drills match the original Gerbers in `../Gerbers/`.

| File | Upload as |
|---|---|
| `nmea0183-adapter-7.1-gerbers-JLCPCB.zip` | Gerber file |
| `nmea0183-adapter-7.1-BOM-JLCPCB.csv` | BOM |
| `nmea0183-adapter-7.1-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 2 layers, **1.0 mm** thick (as in the original Gerber job file), 52.1 x 42.1 mm
- Order number: "Specify a location" (the board has a `JLCJLCJLCJLC` marker)
- PCB assembly: top side only

## Parts

LCSC numbers are stored in the `LCSC` field of each schematic symbol.

Changes from the original design:

| Ref | Original | Fitted | Why |
|---|---|---|---|
| J1 | RJ-82A86MMNL | FG RJ-055-1 (C7205195) | Sunken SMD RJ45; same footprint as the transponder board |
| U3 | ADuM121N (grade not given) | ADuM121N1BRZ (C190783) | "1" grade outputs default high when USB is unplugged, so the transponder's RX idles |
| U6 | DS8921M | DS8921M/NOPB (C133584) | Orderable part number |
| TH1 | generic PTC | BSMD1206-050-16V (C883124) | Same 500 mA polyfuse as the NMEA 2000 adapter |
| LED1-4 | LED (no colour) | green KT-1206G (C14641) | Colour not specified in the design |

### Not assembled by JLCPCB

| Ref | Part | Notes |
|---|---|---|
| J2 | On Shore OSTVN04A150, THT terminal block | 0 stock at JLCPCB; DigiKey ED10563-ND; hand-solder |
| S1, S2 | E-Switch LC1258EENP, THT latching pushbutton | 0 stock at JLCPCB; hand-solder |
| R7, R8 | 0R | DNP in the design |

## Rotations

The CPL rotations have been pre-corrected using the offsets confirmed on the NMEA 2000 board:
SOIC/SO/SOT-23-6 parts (U1, U2, U3, U6) are -90 deg from KiCad; SOT-23/SOT-23-5 parts
(Q1, Q2, U4, U5) are 180 deg from KiCad. The top-side RJ45 (J1) keeps its KiCad rotation.
All verified in JLCPCB's placement preview (Nov 2026).
