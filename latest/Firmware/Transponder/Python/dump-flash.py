#!/usr/bin/env python3
"""Read-only flash dump of an STM32 through the ST ROM bootloader (AN3155).

Use it only after the board's `dfu` command has dropped it into the ST ROM
bootloader. That is the silent, 8E1 bootloader that answers 0x7F with 0x79,
not the "MAIANA bootloader ready" one, which can only write.

This script sends only these commands: sync (0x7F), Get (0x00), Get ID
(0x02) and Read Memory (0x11). It never sends Write, Erase, Go, Readout
Protect or Readout Unprotect. Readout Unprotect would MASS ERASE the chip.
Power-cycle the board afterwards to return to the application.

Usage: dump-flash.py /dev/ttyUSB0 [--size KB] [--out DIR]
"""
import argparse
import datetime
import hashlib
import os
import sys
import time

import serial

ACK, NACK = 0x79, 0x1F
FLASH_BASE = 0x08000000
FLASH_SIZE_REG = 0x1FFF75E0      # STM32L4 flash size in KB (16-bit)
OTP_BASE, OTP_SIZE = 0x1FFF7000, 1024
CHUNK = 256


class BootloaderError(Exception):
    pass


def expect_ack(port, what):
    b = port.read(1)
    if not b:
        raise BootloaderError(f"{what}: no reply (timeout)")
    if b[0] == NACK:
        raise BootloaderError(f"{what}: NACK")
    if b[0] != ACK:
        raise BootloaderError(f"{what}: unexpected byte 0x{b[0]:02x}")


def command(port, code, what):
    port.write(bytes([code, code ^ 0xFF]))
    expect_ack(port, what)


def sync(port):
    port.reset_input_buffer()
    port.write(b"\x7f")
    b = port.read(1)
    # 0x1F after a sync means the bootloader was already synced, which is fine.
    if not b or b[0] not in (ACK, NACK):
        raise BootloaderError(
            "no answer to 0x7F. The board is probably not in the ST ROM "
            "bootloader (or is in the MAIANA bootloader, which cannot read).")


def get(port):
    command(port, 0x00, "Get")
    n = port.read(1)[0]
    data = port.read(n + 1)
    expect_ack(port, "Get (end)")
    return data[0], list(data[1:])


def get_id(port):
    command(port, 0x02, "Get ID")
    n = port.read(1)[0]
    data = port.read(n + 1)
    expect_ack(port, "Get ID (end)")
    return int.from_bytes(data, "big")


def read_mem(port, addr, length):
    assert 1 <= length <= 256
    command(port, 0x11, f"Read Memory @0x{addr:08x}")
    a = addr.to_bytes(4, "big")
    port.write(a + bytes([a[0] ^ a[1] ^ a[2] ^ a[3]]))
    expect_ack(port, f"address 0x{addr:08x}")
    n = length - 1
    port.write(bytes([n, n ^ 0xFF]))
    expect_ack(port, f"length {length}")
    data = port.read(length)
    if len(data) != length:
        raise BootloaderError(f"short read at 0x{addr:08x}")
    return data


def read_region(port, base, size, label):
    out = bytearray()
    for off in range(0, size, CHUNK):
        out += read_mem(port, base + off, min(CHUNK, size - off))
        sys.stderr.write(f"\r{label}: {len(out)}/{size} bytes")
    sys.stderr.write("\n")
    return bytes(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("device")
    ap.add_argument("--size", type=int, help="flash size in KB (default: read from chip)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    port = serial.Serial(args.device, args.baud, timeout=2,
                         parity=serial.PARITY_EVEN, stopbits=1)
    time.sleep(0.1)
    sync(port)
    ver, cmds = get(port)
    pid = get_id(port)
    print(f"bootloader v{ver >> 4}.{ver & 0xF}, PID 0x{pid:03x}, "
          f"commands {' '.join(f'{c:02x}' for c in cmds)}")
    if 0x11 not in cmds:
        sys.exit("Read Memory not offered; stopping.")

    try:
        size_kb = args.size or int.from_bytes(read_mem(port, FLASH_SIZE_REG, 2), "little")
    except BootloaderError as e:
        sys.exit(f"{e}. Read Memory refused: readout protection (RDP) is probably "
                 "on. Do NOT try Readout Unprotect: it mass-erases the chip.")
    print(f"flash size {size_kb} KB")

    flash = read_region(port, FLASH_BASE, size_kb * 1024, "flash")
    path = os.path.join(args.out, f"maiana-flash-{stamp}-pid{pid:03x}.bin")
    with open(path, "wb") as f:
        f.write(flash)
    print(f"wrote {path}  sha256 {hashlib.sha256(flash).hexdigest()}")

    try:
        otp = read_region(port, OTP_BASE, OTP_SIZE, "otp")
        opath = os.path.join(args.out, f"maiana-otp-{stamp}.bin")
        with open(opath, "wb") as f:
            f.write(otp)
        print(f"wrote {opath}  sha256 {hashlib.sha256(otp).hexdigest()}")
    except BootloaderError as e:
        print(f"OTP read skipped: {e}")

    port.close()
    print("Done. Power-cycle the board to return to the application.")


if __name__ == "__main__":
    main()
