# Watch MAIANA serial: print GPS fix/satellite changes and any $PAI / !AIVD lines. Read-only.
import serial, time, sys
s = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
last = None; last_print = 0; sats = '0'
while True:
    line = s.readline().decode(errors='replace').strip()
    if not line: continue
    if line.startswith(('$PAI', '!AIVD')) and not line.startswith('$PAINF'):
        print(line, flush=True); continue
    f = line.split(',')
    if line.startswith('$GPGSV') or line.startswith('$GLGSV'):
        if f[2] == '1' and line.startswith('$GPGSV'): sats = f[3]
    if line[3:6] == 'RMC' and len(f) > 6:
        state = 'FIX' if f[2] == 'A' else 'no fix'
        now = time.time()
        if state != last or now - last_print > 120:
            print(f"{time.strftime('%H:%M:%S')} GPS {state}, GPS sats in view {sats}, utc {f[1]} {f[9]}", flush=True)
            last, last_print = state, now
