# JLCPCB production files: UART breakout 3.0

The board is still an Eagle design (`../UARTBreakout-3.0.brd/.sch`). These files use Peter's
original Eagle CAM output (Gerbers + drill, unchanged) and his pick-and-place data, plus a JLCPCB BOM.

| File | Upload as |
|---|---|
| `uart-breakout-3.0-gerbers-JLCPCB.zip` | Gerber file |
| `uart-breakout-3.0-BOM-JLCPCB.csv` | BOM |
| `uart-breakout-3.0-CPL-JLCPCB.csv` | CPL / pick-and-place |

## PCB options

- 2 layers, 1.6 mm, 55.86 x 17.45 mm
- PCB assembly: top side only (SMD parts)

## Parts

D3 is a 3 V zener (generic in the design); BZT52C3V0S is used.

### Not assembled by JLCPCB (through-hole; hand-solder)

| Ref | Part | Notes |
|---|---|---|
| J2 | Molex 95501-2821 RJ45 (unshielded, THT) | LCSC C19800963 (low stock); order it with the parts, or from DigiKey |
| JP2, JP3 | 1x8 2.54 mm female header | Any 2.54 mm 8-pin female socket header |

## Note

This revision needs 12 V supplied on JP3 (pin 8 = 12 V, pin 7 = GND); USB only powers the CH340.

## Rotations

U1 (SOT-23), U$1 (SOIC-8) and U$4 (SOT-23-6) are rotated -90 deg from Peter's Eagle
pick-and-place data to match JLCPCB's part models (verified in the placement preview, Nov 2026).
