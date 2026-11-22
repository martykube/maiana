# Read-only: stream MAIANA serial, decode AIS type/MMSI (+name for 5/24A/21), print new stations and a 2-min summary.
import serial, time, collections, socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def bits(payload):
    b = ''
    for c in payload:
        v = ord(c) - 48
        if v > 40: v -= 8
        b += format(v, '06b')
    return b
def u(b, s, n): return int(b[s:s+n], 2) if len(b) >= s+n else None
def txt(b, s, n):
    out = ''
    for i in range(s, min(s+n, len(b) - 5), 6):
        v = int(b[i:i+6], 2); out += chr(v + 64 if v < 32 else v)
    return out.strip('@ ').strip()
s = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
seen = {}; count = collections.Counter(); total = 0; t0 = time.time(); last = time.time()
names = {}
while True:
    line = s.readline().decode(errors='replace').strip()
    if line.startswith(('!', '$')):
        try: udp.sendto((line + '\r\n').encode(), ('127.0.0.1', 10110))
        except OSError: pass
    if line.startswith('$PAI') and not line.startswith(('$PAINF',)):
        print(line, flush=True)
    if line.startswith('!AIVDM'):
        f = line.split(',')
        if len(f) < 7 or f[1] != '1': continue  # skip multipart for simplicity
        b = bits(f[5]); typ = u(b, 0, 6); mmsi = u(b, 8, 30)
        if mmsi is None: continue
        total += 1; count[typ] += 1
        name = ''
        if typ == 5: name = txt(b, 112, 120)
        elif typ == 24 and u(b, 38, 2) == 0: name = txt(b, 40, 120)
        elif typ == 21: name = txt(b, 43, 120)
        if name: names[mmsi] = name
        if mmsi not in seen:
            seen[mmsi] = typ
            print(f"{time.strftime('%H:%M:%S')} NEW #{len(seen)} MMSI {mmsi:09d} type {typ} ch {f[4]} {name}", flush=True)
        elif name and names.get(mmsi) == name and seen[mmsi] != 'named':
            seen[mmsi] = 'named'; print(f"{time.strftime('%H:%M:%S')} name MMSI {mmsi:09d} = {name}", flush=True)
    if time.time() - last > 120:
        last = time.time()
        print(f"{time.strftime('%H:%M:%S')} SUMMARY {len(seen)} stations, {total} msgs in {int((last-t0)/60)} min, types {dict(count)}", flush=True)
