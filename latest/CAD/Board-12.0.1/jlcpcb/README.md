# JLCPCB production files: transponder 12.0.1

Generated from the KiCad project in this directory with `kicad-cli` (KiCad 9).

| File | Upload as |
|---|---|
| `transponder-12.0.1-gerbers-JLCPCB.zip` | Gerber file |
| `transponder-12.0.1-BOM-JLCPCB.csv` | BOM |
| `transponder-12.0.1-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 4 layers, 1.6 mm, standard via process (matches Peter's published Gerbers; copper layers regenerated unchanged)
- PCB assembly: **both sides**. J2 (SWD header) is the only bottom-side part.

## Parts

LCSC numbers are stored in the `LCSC` field of each schematic symbol.

Substitutions from the original design (out of stock at JLCPCB, Nov 2026):

| Ref | Original | Fitted | Why it's safe |
|---|---|---|---|
| U5 | STM32L412K8U6 | STM32L412KBU6 (C529439) | Same die and pinout, 128 KB flash; L412 firmware runs unchanged |
| U9, U10 | SI1926DL-T1-E3 | DMN63D8LDW-7 (C211422) | Same dual N-MOSFET SOT-363 pinout; drives LEDs / TX_OFF only |
| J4 | RJ-82A86MMNL | FG RJ-055-1 (C7205195) | Sunken SMD RJ45; pins, pegs, cutout and shield tabs match the footprint |
| J2 | (not fitted) | Samtec FTSH-105-01-L-DV-K (C5155080) | Needed to flash the bootloader on new boards |

Where Murata C0G capacitors were out of stock, Yageo NP0 parts of the same value were used.

### Global Sourcing (no JLCPCB stock; buy from DigiKey through JLCPCB)

| Ref | Part | DigiKey |
|---|---|---|
| AE1 | Johanson 1575AT43A0040001E | 1575AT43A0040001E |
| J3 | RF Solutions CON-SMA-EDGE-S | CON-SMA-EDGE-S-ND |
| U11 | TST TB0436A (162 MHz SAW) | TB0436A (low stock, order early) |
| Y1, Y2 | ECS-300-10-33B-CKM-TR | keep this exact crystal; a different crystal shifts frequency (issue #103) |

### To confirm before ordering

- **L4** (2.2 µH, PA drain choke): the schematic has no manufacturer part; the BOM uses
  FH CMH160808B2R2MT (750 mA) as a placeholder. Confirm with the original designer.
- **Rotations**: check every part in JLCPCB's placement preview, especially QFN, SOT-23/89/363,
  the RJ45 and the bottom-side J2. KiCad and JLCPCB use different zero orientations for some packages.
