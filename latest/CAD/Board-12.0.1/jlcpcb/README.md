# JLCPCB production files: transponder 12.0.1

Generated from the KiCad project in this directory with `kicad-cli` (KiCad 9).

| File | Upload as |
|---|---|
| `transponder-12.0.1-gerbers-JLCPCB.zip` | Gerber file |
| `transponder-12.0.1-BOM-JLCPCB.csv` | BOM |
| `transponder-12.0.1-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 4 layers, 1.6 mm, standard via process (matches Peter's published Gerbers; copper layers regenerated unchanged)
- PCB assembly: **both sides**. Everything is on top except J2, the SWD header, on the bottom.
  J2 is fitted so every board can take the bootloader over SWD (see the last section).

## Parts

LCSC numbers are stored in the `LCSC` field of each schematic symbol.

Substitutions from the original design (out of stock at JLCPCB, Nov 2026):

| Ref | Original | Fitted | Why it's safe |
|---|---|---|---|
| U5 | STM32L412K8U6 | STM32L412KBU6 (C529439) | Same die and pinout, 128 KB flash; L412 firmware runs unchanged |
| U9, U10 | SI1926DL-T1-E3 | DMN63D8LDW-7 (C211422) | Same dual N-MOSFET SOT-363 pinout; drives LEDs / TX_OFF only |
| J4 | RJ-82A86MMNL | FG RJ-055-1 (C7205195) | Sunken SMD RJ45; pins, pegs, cutout and shield tabs match the footprint |
| J2 | (unfitted) | Samtec FTSH-105-01-L-DV-K-TR (C448647) | 2x5 1.27 mm SMD header for SWD; fallback C5155080 is the same part, not on tape |

Where Murata C0G capacitors were out of stock, Yageo NP0 parts of the same value were used.

### Sourced separately (no JLCPCB stock when ordered, Nov 2026)

These are bought into My Parts Lib through JLCPCB, then assigned to the board in the BOM step.
They can only be used in JLCPCB assembly orders. Until they arrive they show as a shortfall.

| Ref | Part | JLCPCB # | Source | Qty |
|---|---|---|---|---:|
| U11 | TST TB0436A (162 MHz SAW) | C6279566 | JLCPCB Request Quote (pre-order) | 7 |
| AE1 | Johanson 1575AT43A0040001E | C17625601 | Global Sourcing: Element | 7 |
| J3 | RF Solutions CON-SMA-EDGE-S | C5356059 | Global Sourcing: RS Components | 7 |
| Y1, Y2 | ECS-300-10-33B-CKM-TR | C2450899 | Global Sourcing: DigiKey XC2521CT-ND | 12 |

- **U11**: Part Request came back unavailable, DigiKey is 500 minimum, and no drop-in 162 MHz
  alternative was found. The Request Quote form worked: $13.01 each against a $1.52 catalogue price.
- **Y1, Y2**: keep this exact crystal; a different crystal shifts frequency (issue #103).

### Notes on specific parts

- **L4** (2.2 µH, PA drain choke, V_PA ≈ 4.6 V → Q1 drain): the schematic gives no part number.
  Peter's 10.5 BOM used Taiyo Yuden BRC2012T2R2MD (0805, ~1.1 A); 12.0.1 has an 0603 footprint, so
  APV AFL160808-2R2MLH (C55265173, 0603, Isat 1.4 A, 270 mΩ) is fitted. TX bursts draw up to ~0.8 A.

## Rotations

The CPL rotations are corrected for JLCPCB's part models. Do not regenerate the CPL from KiCad
without re-applying these. Check each part in JLCPCB's placement preview, where the pin-1 dot
should sit on the footprint's pin-1 pad; offsets depend on the part's model, not only its package.

| Parts | Offset from KiCad |
|---|---|
| Q1, Q2, Q7 | 180 deg |
| CR1, IC1, U3, U5, U6, U7, U8, U9, U10, U12 | -90 deg |
| J4 and all other placed parts | unchanged |

Verified in the preview (Nov 2026), except for **AE1, J2, J3, U11, Y1 and Y2**: the preview doesn't
show them until they are in My Parts Lib and selected, so check them before ordering. D1 is
bidirectional, so its direction doesn't matter.

U5 has no package marking in JLCPCB's model, so its rotation relies on the pin-1 dot, which agrees
with the footprint and the silkscreen dot. Confirm U5 in JLCPCB's DFM review after ordering.

## Flashing the bootloader on new boards

J2 is a 2x5 1.27 mm ARM Cortex SWD 10-pin header on the bottom side (pin 1 3.3 V, 2 SWDIO, 4 SWCLK,
10 NRST, 3/5/9 GND). Plug a 10-pin 1.27 mm IDC cable from the ST-Link onto it to write the
bootloader once; after that, firmware updates go over the UART. The ST-Link does not power the
board, so supply 12 V separately.

A pogo-pin edge clip is not recommended: the footprint is `PinHeader_2x05_P1.27mm_Vertical_SMD`,
whose pads sit 0.75-3.15 mm from the row centre line, while a 1.27 mm clip's pins sit at 0.635 mm,
just inside the pads' inner ends. The original boards have the same bare pads; to back one up
over SWD, hand-solder the same header.

J2's CPL rotation (-90, bottom) is KiCad's raw value and is unchecked; confirm pin 1 in the
bottom-side preview. J2 was added to the BOM and CPL by hand; the schematic symbol is still marked
unfitted, so re-add these two rows if the files are ever regenerated.
