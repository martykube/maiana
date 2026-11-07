# Solder practice board

A bare two-layer PCB for practicing through-hole soldering before working on the breakouts.
It uses the same footprints as the real boards. No assembly: all parts are hand-soldered.

## Ordering

Upload `jlcpcb/solder-practice-gerbers-JLCPCB.zip` to JLCPCB.

- 100 x 76 mm, 2 layers, 1.6 mm, HASL, any mask color
- PCB assembly: off

## Sections

| # | Section | Part to use | Same as |
|---|---|---|---|
| 1 | Resistors | Any 1/4 W axial, 10.16 mm spacing | Warm-up |
| 2 | Headers | 1x8 2.54 mm headers | UART JP2, JP3 |
| 3 | DIP-8 | DIP-8 socket; make a bridge, then clear it with wick | Warm-up |
| 4 | Heavy pins | Any header pins. RELIEF has thermal spokes, SOLID ties straight to the planes | Heat load comparison |
| 5 | Terminal | On Shore OSTVN04A150 | NMEA 0183 J2 |
| 6 | Button | E-Switch LC1258EENP | NMEA 0183 S1, S2 |
| 7 | RJ45 | Molex 95501-2881 | UART J2 |
| 8 | M12 | M12 sample, mounted on the back | NMEA 2000 J1 |

On sections 2, 5, 6, 7 and 8, one pin connects to the ground planes, as on the real boards, so it
takes more heat. No section is a working circuit.

## Regenerating

`python3 generate.py` rebuilds the board with KiCad 9's `pcbnew` module, copying footprints from the
NMEA 0183, NMEA 2000 and transponder boards. Re-export the Gerbers and drills after running it.
The RJ45 footprint comes from the Eagle pad data in `UARTBreakout-3.0.brd`.
