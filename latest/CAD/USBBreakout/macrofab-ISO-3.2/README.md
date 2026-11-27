# MacroFab quote files: USB breakout ISO 3.2 (DRAFT, benchmark quote only)

Made 2026-11-27 from Peter's Eagle board (`../USBBreakout-ISO-3.2.brd`) and CAM Gerbers.
The real order stays at JLCPCB (`../jlcpcb-ISO-3.2`): U1 and the switches are already in My Parts Lib there.

| File | What |
|---|---|
| `usb-breakout-iso-3.2-gerbers-MacroFab.zip` | Peter's Gerbers renamed to Protel extensions (GTL/GBL/GTO/GBO/GTS/GBS/GTP/GBP, BOR = outline, XLN = Excellon drill) |
| `usb-breakout-iso-3.2.XYRS` | Placements, tab-separated, mils, Eagle origin; Side 1 = top, 2 = bottom; Type 1 = SMD, 2 = PTH; sizes = pad extents |
| `usb-breakout-iso-3.2-BOM-MacroFab.csv` | 17 lines, manufacturer + MPN (passives = the LCSC parts' MPNs) |

Board: 2 layers, 1.6 mm, 38 x 48 mm, both sides (J2 micro-USB and J3 RJ45 bottom SMD, J1 terminal block THT).
Unlike the JLC order, J1 is included for machine/hand assembly.

Checked 2026-11-27 against MacroFab's "Required Design Files" article: Gerber extensions, BOR outline,
XLN drill and the XYRS columns/units/side/type codes match. Their BOM upload must be .xlsx; the XYRS
already carries MPNs, so the CSV here is a reference only.

**Easiest route:** MacroFab reads Eagle boards directly: upload `../USBBreakout-ISO-3.2.brd`.
Use the Gerber zip + XYRS only if the .brd import goes wrong. Either way, check bottom-side
rotations (J2, J3) and J1 in their placement viewer.

## Parts DigiKey and Mouser don't stock (checked 2026-11-27)

MacroFab buys from US distributors, so these need consigning (LCSC) or a substitute:

| Ref | Part | Note |
|---|---|---|
| U1 | 2Pai PI122U31 (isolator) | possible drop-in: ADuM1201 / Si8621 class, pinout NOT checked |
| U2 | WCH CH340N | no US source; consign from LCSC |
| U3 | Seaward SE8533X2-HF (LDO) | substitute needed |
| D2 | WILLSEMI WSB5508L-2/TR | substitute needed |
| F1 | BHFUSE BSMD1206-050-16V | substitute (any 1206 PTC 0.5 A hold) |
| GPS/PWR/RX/TX | TJ-S3216CL9T5ALC2G-A5 green 1206 LED | any 1206 green LED |
| J3 | Pulse RJ-82A86MMNL | not stocked; JLC build uses FG RJ-055-1 |

In stock in the US: CL-SB-12B-01T, 10118194-0001LF, OSTVN02A150, SI2307CDS-T1-E3 (plus generic passives, SMBJ14CA, BSS138).

## Benchmark quote (2026-11-27)

MacroFab imported the Eagle .brd directly (PCB "MAIANA USB Breakout ISO 3.2", not ordered).
Qty 5, incomplete BOM (12 of 17 lines unpriced: passives/LEDs/Q4 need house parts; U1, U2, J3 unsourced;
D2, F1, U3 lead time unknown): $715.97 at 24 business days, $932.46 at 18, $1,001.99 at 15, $2,673.90 at 10.
Decision: stay with JLCPCB for this board.
