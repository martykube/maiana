# usage: python3 -I mcli.py 'tx?' ['station?' ...]  -> prints $PAI replies (read-only queries only)
import serial, sys, time
s = serial.Serial('/dev/ttyUSB0', 38400, timeout=0.2)
time.sleep(0.3); s.reset_input_buffer()
out = b''
for cmd in sys.argv[1:]:
    s.write(cmd.encode() + b'\r\n'); t = time.time()
    while time.time() - t < 1.5: out += s.read(512)
s.close()
for line in out.decode(errors='replace').splitlines():
    if not line.startswith('$G'): print(line)
